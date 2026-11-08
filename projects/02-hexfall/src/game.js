// The game state: map, units, turns, undo and serialisation. DOM-free and deterministic.
import { generate } from "./mapgen.js";
import { HexMap } from "./map.js";
import { RNG } from "./rng.js";
import { key, distance, neighbors } from "./hex.js";
import { createUnit, maxMp, maxHp, healAmount, unitType, DEFAULT_ARMY, RECRUITABLE, UNIT_TYPES } from "./units.js";
import {
  DEFAULT_RULES, capture, income, holdTarget, ownedVillages, recruitHexes, recruitProblem, score,
} from "./economy.js";
import { timeOfDay } from "./timeofday.js";
import { movementArea, routeTo, destinations, enemyZoc } from "./movement.js";
import { attackKind, forecast, resolveAttack } from "./combat.js";
import { useAbility as applyAbility, abilityTargets, abilityProblem, tickCooldowns } from "./abilities.js";
import { tick as tickStatuses, poisonTick, hasStatus, removeStatus, adjustedMp } from "./status.js";
import { visibleHexes } from "./fog.js";
import { currentWeather } from "./weather.js";
import { FLAMMABLE, FIRE_DAMAGE } from "./terrain.js";

export const SIDES = Object.freeze([
  { id: "red", name: "Red" },
  { id: "blue", name: "Blue" },
]);
export const VILLAGE_HEAL = 8;
export const SAVE_VERSION = 3;
export const FIRE_SPREAD = 0.2; // chance per round that a burning hex lights each flammable neighbour
const CHEAPEST = Math.min(...Object.values(UNIT_TYPES).map((t) => t.cost));

export class Game {
  /**
   * @param {object} init
   * @param {HexMap} init.map
   * @param {Array<Array<{q:number,r:number}>>} init.spawns  deployment zone per side
   * @param {number} [init.seed]
   * @param {object} [init.rules]  overrides for DEFAULT_RULES (gold, income, objectives)
   */
  constructor({ map, spawns, villages = [], seed = 1, rules = {} }) {
    this.map = map;
    this.spawns = spawns;
    this.villages = villages;
    this.seed = seed;
    this.rng = new RNG(seed ^ 0x5bd1e995);
    this.units = [];
    this.nextId = 1;
    this.turn = 1;
    this.active = 0;           // index into SIDES
    this.winner = null;        // side id once decided
    this.log = [];             // {turn, side, text}
    this.history = [];         // undo stack of moves since the last irreversible action
    this.rules = { ...DEFAULT_RULES, ...rules };
    this.sideIds = SIDES.map((s) => s.id);
    this.gold = SIDES.map(() => this.rules.startGold);
    this.hold = SIDES.map(() => 0); // consecutive own turn starts holding enough villages
    this.endReason = null;     // "rout" | "hold" | "turns" once decided
    this.explored = SIDES.map(() => new Set()); // fog of war: hexes each side has ever seen
    this.stamp = 0;            // bumped on every state change (vision cache key)
    this.visCache = new Map();
  }

  /**
   * A new skirmish on a generated map with both armies deployed.
   * @param {object} [opts] {seed, symmetric, armies: [string[], string[]], map: generator options}
   */
  static create(opts = {}) {
    const seed = opts.seed ?? 1;
    const gen = generate({ seed, symmetric: opts.symmetric ?? false, ...(opts.map ?? {}) });
    const game = new Game({ map: gen.map, spawns: gen.spawns, villages: gen.villages, seed, rules: opts.rules });
    const armies = opts.armies ?? [DEFAULT_ARMY, DEFAULT_ARMY];
    armies.forEach((army, i) => game.deploy(SIDES[i].id, army));
    game.say(`Battle begins on map ${seed}. ${SIDES[0].name} moves first.`);
    game.updateVision();
    return game;
  }

  get side() {
    return SIDES[this.active].id;
  }

  sideIndex(id) {
    return SIDES.findIndex((s) => s.id === id);
  }

  say(text) {
    this.log.push({ turn: this.turn, side: this.side, text });
    if (this.log.length > 500) this.log.splice(0, this.log.length - 500);
  }

  /** Place `types` for `side` on its deployment zone (nearest-to-camp hexes first). */
  deploy(side, types) {
    const zone = this.spawns[this.sideIndex(side)];
    const free = zone.filter((h) => !this.unitAt(h) && this.map.passable(h));
    if (types.length > free.length) throw new Error(`${side} has ${types.length} units but only ${free.length} deployment hexes`);
    return types.map((type, i) => {
      const u = createUnit(this.nextId++, type, side, free[i]);
      this.units.push(u);
      return u;
    });
  }

  unitAt(h) {
    return this.units.find((u) => u.q === h.q && u.r === h.r && u.hp > 0) ?? null;
  }

  unitById(id) {
    return this.units.find((u) => u.id === id) ?? null;
  }

  unitsOf(side) {
    return this.units.filter((u) => u.side === side);
  }

  /** Units of the active side that can still move or attack. */
  ready() {
    return this.unitsOf(this.side).filter((u) => u.mp > 0 || (!u.acted && this.targets(u).length));
  }

  /** Movement area of `unit` (empty beyond its own hex when it is not its turn). */
  area(unit) {
    if (unit.side !== this.side || this.winner) return new Map([[key(unit), { hex: { q: unit.q, r: unit.r }, cost: 0, prev: null, zoc: false, canStop: true }]]);
    return movementArea(this, unit, { ignore: this.hiddenIds(unit.side) });
  }

  // ------------------------------------------------------------ fog of war

  /** Hex keys `side` sees right now (null when fog of war is off = everything). */
  visible(side) {
    if (!this.rules.fog) return null;
    const cached = this.visCache.get(side);
    if (cached && cached.stamp === this.stamp) return cached.set;
    const set = visibleHexes(this, side);
    this.visCache.set(side, { stamp: this.stamp, set });
    return set;
  }

  /** Can `side` see unit (or hex) `u`? Always true without fog; a side always sees its own units. */
  isVisible(side, u) {
    if (!this.rules.fog || u.side === side) return true;
    return this.visible(side).has(key(u));
  }

  /** Ids of enemy units `side` cannot see (null without fog). */
  hiddenIds(side) {
    if (!this.rules.fog) return null;
    const vis = this.visible(side);
    return new Set(this.units.filter((u) => u.side !== side && !vis.has(key(u))).map((u) => u.id));
  }

  /** Has `side` ever seen hex `h`? */
  isExplored(side, h) {
    return !this.rules.fog || this.explored[this.sideIndex(side)].has(key(h));
  }

  /** Something changed: drop cached vision and add what each side sees now to its memory. */
  updateVision() {
    this.stamp += 1;
    if (!this.rules.fog) return;
    SIDES.forEach((s, i) => { for (const k of this.visible(s.id)) this.explored[i].add(k); });
  }

  /** Is `unit` standing in an enemy zone of control? */
  inZoc(unit) {
    return enemyZoc(this, unit.side).has(key(unit));
  }

  /** Move `unit` to `dest` along its cheapest route. Returns the route, or throws. */
  move(unit, dest) {
    if (this.winner) throw new Error("the battle is over");
    if (unit.side !== this.side) throw new Error("not this unit's turn");
    if (unit.acted) throw new Error("unit has already attacked this turn");
    const area = this.area(unit);
    let route = routeTo(area, dest);
    if (!route) throw new Error(`unit ${unit.id} cannot reach ${key(dest)}`);
    if (route.length === 1) return route;
    const ambush = this.ambushStop(unit, route);
    if (ambush) {
      route = route.slice(0, ambush.index + 1);
      dest = route[route.length - 1];
    }
    const node = area.get(key(dest));
    const entry = { id: unit.id, q: unit.q, r: unit.r, mp: unit.mp, moved: unit.moved ?? false };
    this.history.push(entry);
    unit.q = dest.q;
    unit.r = dest.r;
    unit.moved = true;
    unit.mp = node.zoc || ambush ? 0 : Math.max(0, unit.mp - node.cost);
    if (ambush) {
      this.say(`Ambush! ${SIDES[this.active].name}'s ${unitType(unit).name.toLowerCase()} runs into a hidden enemy.`);
      this.history = []; // what was revealed cannot be unseen
    }
    const prev = capture(this, unit.side, dest);
    if (prev !== undefined) {
      entry.capturedFrom = prev;     // undo gives the village back
      unit.mp = 0;                   // capturing a village ends the move
      this.say(`${SIDES[this.active].name} captures a village${prev ? ` from ${this.sideName(prev)}` : ""} (${ownedVillages(this, unit.side).length} held).`);
    }
    this.updateVision();
    return route;
  }

  /**
   * Under fog of war, where does a route run into an enemy the mover could not see? The unit
   * stops on the first hex next to a hidden enemy (its zone of control; skirmishers slip past
   * those) or just before a hex a hidden enemy stands on. Returns {index} into the route or null.
   */
  ambushStop(unit, route) {
    const hidden = this.hiddenIds(unit.side);
    if (!hidden?.size) return null;
    const foes = this.units.filter((u) => hidden.has(u.id));
    const at = new Set(foes.map(key));
    const zoc = new Set(foes.flatMap((u) => neighbors(u).map(key)));
    const skirmisher = unitType(unit).traits.includes("skirmisher");
    for (let i = 1; i < route.length; i++) {
      if (at.has(key(route[i]))) return { index: i - 1 };
      if (!skirmisher && zoc.has(key(route[i]))) return { index: i };
    }
    return null;
  }

  canUndo() {
    return this.history.length > 0;
  }

  /** Take back the last move (moves are reversible until someone attacks or the turn ends). */
  undo() {
    const last = this.history.pop();
    if (!last) return false;
    const u = this.unitById(last.id);
    if ("capturedFrom" in last) this.map.get(u).owner = last.capturedFrom;
    Object.assign(u, { q: last.q, r: last.r, mp: last.mp, moved: last.moved ?? false });
    this.updateVision();
    return true;
  }

  /** Enemy units `unit` can attack from where it stands. */
  targets(unit, from = unit) {
    if (unit.acted || unit.side !== this.side || this.winner) return [];
    return this.units.filter((t) => t.side !== unit.side && this.isVisible(unit.side, t) && attackKind(this, unit, t, from));
  }

  /**
   * Where should `unit` attack `target` from? Its own hex if possible, otherwise the reachable
   * hex with the best forecast (most expected damage dealt minus taken, then best terrain
   * defence, then the cheapest move). Returns {from, forecast} or null.
   */
  attackPlan(unit, target) {
    if (unit.acted || unit.side !== this.side || target.side === unit.side || this.winner) return null;
    if (!this.isVisible(unit.side, target)) return null;
    const here = forecast(this, unit, target);
    if (here) return { from: { q: unit.q, r: unit.r }, forecast: here };
    let best = null;
    for (const node of destinations(this.area(unit))) {
      if (distance(node.hex, target) > 6) continue;
      const f = forecast(this, unit, target, node.hex);
      if (!f) continue;
      const score = f.expectedDealt - f.expectedTaken + f.killChance * 10 - f.deathChance * 20;
      const def = this.map.terrainAt(node.hex).defense;
      const cand = { from: node.hex, forecast: f, score, def, cost: node.cost };
      if (!best || cand.score > best.score + 1e-9 || (Math.abs(cand.score - best.score) < 1e-9
          && (cand.def > best.def || (cand.def === best.def && cand.cost < best.cost)))) best = cand;
    }
    return best ? { from: best.from, forecast: best.forecast } : null;
  }

  /** Attack `target` with `unit` (moving first if the plan needs it). Returns the result. */
  attack(unit, target) {
    const plan = this.attackPlan(unit, target);
    if (!plan) throw new Error(`unit ${unit.id} cannot attack unit ${target.id}`);
    if (key(plan.from) !== key(unit)) this.move(unit, plan.from);
    const res = resolveAttack(this, unit, target);
    unit.acted = true;
    unit.mp = 0;
    this.history = [];
    for (const line of res.lines) this.say(line);
    this.checkWinner();
    this.updateVision();
    return res;
  }

  // ------------------------------------------------------------ abilities

  /** Hexes `unit` can target with ability `id` from where it stands. */
  abilityTargets(unit, id) {
    return abilityTargets(this, unit, id);
  }

  /** Why `unit` cannot use `id` right now ("" = it can, given a target). */
  abilityProblem(unit, id) {
    return abilityProblem(this, unit, id);
  }

  /** Use ability `id` of `unit` on hex `target`. Spends the unit's action. */
  useAbility(unit, id, target) {
    const res = applyAbility(this, unit, id, target);
    this.history = [];
    for (const line of res.lines) this.say(line);
    this.checkWinner();
    this.updateVision();
    return res;
  }

  sideName(id) {
    return SIDES.find((s) => s.id === id)?.name ?? id;
  }

  /** Current time of day (dawn, morning, ... second watch). */
  timeOfDay() {
    return timeOfDay(this.turn);
  }

  /** Can side index `i` still field an army (units left, or gold and a keep to recruit)? */
  canFight(i) {
    if (this.unitsOf(SIDES[i].id).length) return true;
    return this.gold[i] >= CHEAPEST && recruitHexes(this, i).length > 0;
  }

  /** Declare the result once. `winner` may be "draw". */
  finish(winner, reason, text) {
    if (this.winner) return;
    this.winner = winner;
    this.endReason = reason;
    this.history = [];
    this.say(text);
  }

  checkWinner() {
    const alive = SIDES.filter((_s, i) => this.canFight(i));
    if (alive.length === 1 && !this.winner) {
      this.finish(alive[0].id, "rout", `${alive[0].name} wins — the enemy army is routed!`);
    }
    return this.winner;
  }

  // ------------------------------------------------------------ economy

  /** Why the active side cannot recruit `type` now ("" = it can). */
  recruitProblem(type) {
    if (this.winner) return "the battle is over";
    if (!RECRUITABLE.includes(type)) return `cannot recruit ${type}`;
    return recruitProblem(this, this.active, type);
  }

  /** Free hexes where the active side can place recruits. */
  recruitHexes() {
    return this.winner ? [] : recruitHexes(this, this.active);
  }

  /**
   * Recruit a `type` unit for the active side on `at` (default: the free castle hex nearest
   * the enemy). Costs gold; the recruit cannot move or attack until the next turn.
   */
  recruit(type, at = null) {
    const problem = this.recruitProblem(type);
    if (problem) throw new Error(`cannot recruit ${type}: ${problem}`);
    const hexes = this.recruitHexes();
    let hex;
    if (at) {
      hex = hexes.find((h) => h.q === at.q && h.r === at.r);
      if (!hex) throw new Error(`cannot recruit on ${key(at)}`);
    } else {
      const foe = this.spawns[(this.active + 1) % SIDES.length]?.[0];
      hex = foe ? hexes.slice().sort((a, b) => distance(a, foe) - distance(b, foe))[0] : hexes[0];
    }
    const u = createUnit(this.nextId++, type, this.side, hex);
    u.mp = 0;
    u.acted = true;
    this.units.push(u);
    this.gold[this.active] -= unitType(type).cost;
    this.history = [];
    this.updateVision();
    this.say(`${SIDES[this.active].name} recruits a ${unitType(type).name.toLowerCase()} (${this.gold[this.active]} gold left).`);
    return u;
  }

  /** Battle score of a side (used when the turn limit is reached). */
  score(side) {
    return score(this, side);
  }

  /** Villages needed for a hold victory (0 = disabled). */
  holdTarget() {
    return holdTarget(this);
  }

  /** Turn limit reached: the higher score wins. */
  decideOnScore() {
    const [a, b] = SIDES.map((s) => this.score(s.id).total);
    const text = `Turn limit reached — score ${SIDES[0].name} ${a} : ${b} ${SIDES[1].name}.`;
    if (a === b) this.finish("draw", "turns", `${text} The battle is a draw.`);
    else this.finish(a > b ? SIDES[0].id : SIDES[1].id, "turns", `${text} ${a > b ? SIDES[0].name : SIDES[1].name} wins on points!`);
  }

  /** End the active side's turn and start the next side's (healing, fresh move points). */
  endTurn() {
    if (this.winner) return;
    this.history = [];
    tickStatuses(this.unitsOf(this.side), "end");
    this.active = (this.active + 1) % SIDES.length;
    if (this.active === 0) {
      if (this.rules.turnLimit && this.turn >= this.rules.turnLimit) {
        this.decideOnScore();
        return;
      }
      this.turn += 1;
      this.burnRound();
    }
    this.say(`Turn ${this.turn} (${this.timeOfDay().name}): ${SIDES[this.active].name} to move.`);
    this.startTurn();
  }

  /**
   * Start-of-turn upkeep for the active side: income, the village hold count (and hold
   * victory), village and healer healing, fresh move points.
   */
  startTurn() {
    const gained = income(this, this.side);
    this.gold[this.active] += gained;
    const held = ownedVillages(this, this.side).length;
    const target = this.holdTarget();
    if (target && held >= target) {
      this.hold[this.active] += 1;
      const left = this.rules.holdTurns - this.hold[this.active];
      if (left <= 0) {
        this.finish(this.side, "hold", `${SIDES[this.active].name} wins — ${held} villages held for ${this.rules.holdTurns} turns!`);
        return;
      }
      this.say(`${SIDES[this.active].name} holds ${held}/${this.villages.length} villages: ${left} more turn${left === 1 ? "" : "s"} to victory.`);
    } else {
      this.hold[this.active] = 0;
    }
    this.say(`${SIDES[this.active].name} collects ${gained} gold (${this.gold[this.active]} total).`);
    const mine = this.unitsOf(this.side);
    // burning ground and poison hurt first (never below 1 HP)
    for (const u of mine) {
      if (this.map.get(u)?.fire > 0) {
        const lost = Math.min(FIRE_DAMAGE, u.hp - 1);
        if (lost > 0) {
          u.hp -= lost;
          this.say(`${u.side} ${unitType(u).name.toLowerCase()} #${u.id} is burned for ${lost}.`);
        }
      }
    }
    const heals = new Map();
    for (const u of mine) {
      if (this.map.get(u)?.terrain === "village") heals.set(u.id, VILLAGE_HEAL);
    }
    for (const healer of mine) {
      const amount = healAmount(healer);
      if (!amount) continue;
      for (const n of neighbors(healer)) {
        const ally = this.unitAt(n);
        if (ally && ally.side === healer.side) heals.set(ally.id, Math.max(heals.get(ally.id) ?? 0, amount));
      }
    }
    for (const u of mine) {
      const label = `${u.side} ${unitType(u).name.toLowerCase()} #${u.id}`;
      if (hasStatus(u, "poisoned")) {
        if (heals.has(u.id)) {
          removeStatus(u, "poisoned");
          this.say(`${label} is cured of poison.`);
        } else {
          const lost = poisonTick(u);
          if (lost) this.say(`${label} suffers ${lost} poison damage.`);
        }
      } else {
        const amount = Math.min(heals.get(u.id) ?? 0, maxHp(u) - u.hp);
        if (amount > 0) {
          u.hp += amount;
          this.say(`${label} heals ${amount}.`);
        }
      }
    }
    tickStatuses(mine, "start");
    for (const u of mine) {
      tickCooldowns(u);
      u.mp = adjustedMp(u, maxMp(u));
      u.acted = false;
      u.moved = false;
    }
    this.updateVision();
  }

  /** Current weather (clear, rain, fog, storm). */
  weather() {
    return currentWeather(this);
  }

  /**
   * Once per round (when a new turn number starts): rain and storms put out every fire;
   * otherwise each burning hex may light its flammable neighbours, then burns down by one
   * turn — a forest that burns out becomes open plains.
   */
  burnRound() {
    const burning = this.map.burning();
    if (!burning.length) return;
    if (this.weather().wet) {
      for (const t of burning) delete t.fire;
      this.say(`The ${this.weather().name.toLowerCase()} puts out ${burning.length} fire${burning.length === 1 ? "" : "s"}.`);
      return;
    }
    const lit = [];
    for (const t of burning) {
      for (const n of this.map.neighbors(t)) {
        const nt = this.map.get(n);
        if (FLAMMABLE.has(nt.terrain) && !(nt.fire > 0) && !lit.includes(nt) && this.rng.chance(FIRE_SPREAD)) lit.push(nt);
      }
    }
    for (const t of burning) {
      t.fire -= 1;
      if (t.fire <= 0) {
        delete t.fire;
        if (t.terrain === "forest") t.terrain = "plains";
      }
    }
    for (const t of lit) t.fire = 2;
    if (lit.length) this.say(`The fire spreads to ${lit.length} more hex${lit.length === 1 ? "" : "es"}.`);
  }

  /** Plain JSON-safe snapshot (the undo history is not saved). */
  toJSON() {
    return {
      version: SAVE_VERSION,
      seed: this.seed,
      map: this.map.toJSON(),
      spawns: this.spawns,
      villages: this.villages,
      rng: this.rng.state,
      units: this.units,
      nextId: this.nextId,
      turn: this.turn,
      active: this.active,
      winner: this.winner,
      endReason: this.endReason,
      rules: this.rules,
      gold: this.gold,
      hold: this.hold,
      explored: this.explored.map((s) => [...s]),
      log: this.log,
    };
  }

  static fromJSON(data) {
    if (!data || ![1, 2, SAVE_VERSION].includes(data.version)) throw new Error("unsupported save version");
    const g = new Game({ map: HexMap.fromJSON(data.map), spawns: data.spawns, villages: data.villages, seed: data.seed, rules: data.rules });
    g.rng.state = data.rng >>> 0;
    g.units = structuredClone(data.units);
    Object.assign(g, { nextId: data.nextId, turn: data.turn, active: data.active, winner: data.winner, log: structuredClone(data.log) });
    // version 1 saves predate the economy: they keep the default starting gold
    if (data.gold) g.gold = [...data.gold];
    if (data.hold) g.hold = [...data.hold];
    g.endReason = data.endReason ?? (data.winner ? "rout" : null);
    // version 3 added statuses, cooldowns and fog memory; older units get empty tables
    for (const u of g.units) {
      u.status ??= {};
      u.cd ??= {};
      u.moved ??= false;
    }
    if (data.explored) g.explored = data.explored.map((ks) => new Set(ks));
    // older saves predate weather: keep their battles as they were
    if (data.version < 3) g.rules.weather = data.rules?.weather ?? false;
    g.updateVision();
    return g;
  }
}
