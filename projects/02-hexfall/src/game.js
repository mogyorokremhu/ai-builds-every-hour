// The game state: map, units, turns, undo and serialisation. DOM-free and deterministic.
import { generate } from "./mapgen.js";
import { HexMap } from "./map.js";
import { RNG } from "./rng.js";
import { key, distance, neighbors } from "./hex.js";
import { createUnit, maxMp, maxHp, healAmount, unitType, DEFAULT_ARMY } from "./units.js";
import { movementArea, routeTo, destinations, enemyZoc } from "./movement.js";
import { attackKind, forecast, resolveAttack } from "./combat.js";

export const SIDES = Object.freeze([
  { id: "red", name: "Red" },
  { id: "blue", name: "Blue" },
]);
export const VILLAGE_HEAL = 8;
export const SAVE_VERSION = 1;

export class Game {
  /**
   * @param {object} init
   * @param {HexMap} init.map
   * @param {Array<Array<{q:number,r:number}>>} init.spawns  deployment zone per side
   * @param {number} [init.seed]
   */
  constructor({ map, spawns, villages = [], seed = 1 }) {
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
  }

  /**
   * A new skirmish on a generated map with both armies deployed.
   * @param {object} [opts] {seed, symmetric, armies: [string[], string[]], map: generator options}
   */
  static create(opts = {}) {
    const seed = opts.seed ?? 1;
    const gen = generate({ seed, symmetric: opts.symmetric ?? false, ...(opts.map ?? {}) });
    const game = new Game({ map: gen.map, spawns: gen.spawns, villages: gen.villages, seed });
    const armies = opts.armies ?? [DEFAULT_ARMY, DEFAULT_ARMY];
    armies.forEach((army, i) => game.deploy(SIDES[i].id, army));
    game.say(`Battle begins on map ${seed}. ${SIDES[0].name} moves first.`);
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
    return movementArea(this, unit);
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
    const area = movementArea(this, unit);
    const route = routeTo(area, dest);
    if (!route) throw new Error(`unit ${unit.id} cannot reach ${key(dest)}`);
    if (route.length === 1) return route;
    const node = area.get(key(dest));
    this.history.push({ id: unit.id, q: unit.q, r: unit.r, mp: unit.mp });
    unit.q = dest.q;
    unit.r = dest.r;
    unit.mp = node.zoc ? 0 : Math.max(0, unit.mp - node.cost);
    return route;
  }

  canUndo() {
    return this.history.length > 0;
  }

  /** Take back the last move (moves are reversible until someone attacks or the turn ends). */
  undo() {
    const last = this.history.pop();
    if (!last) return false;
    const u = this.unitById(last.id);
    Object.assign(u, { q: last.q, r: last.r, mp: last.mp });
    return true;
  }

  /** Enemy units `unit` can attack from where it stands. */
  targets(unit, from = unit) {
    if (unit.acted || unit.side !== this.side || this.winner) return [];
    return this.units.filter((t) => t.side !== unit.side && attackKind(this, unit, t, from));
  }

  /**
   * Where should `unit` attack `target` from? Its own hex if possible, otherwise the reachable
   * hex with the best forecast (most expected damage dealt minus taken, then best terrain
   * defence, then the cheapest move). Returns {from, forecast} or null.
   */
  attackPlan(unit, target) {
    if (unit.acted || unit.side !== this.side || target.side === unit.side || this.winner) return null;
    const here = forecast(this, unit, target);
    if (here) return { from: { q: unit.q, r: unit.r }, forecast: here };
    let best = null;
    for (const node of destinations(movementArea(this, unit))) {
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
    return res;
  }

  checkWinner() {
    const alive = SIDES.filter((s) => this.unitsOf(s.id).length > 0);
    if (alive.length === 1 && !this.winner) {
      this.winner = alive[0].id;
      this.say(`${alive[0].name} wins — the enemy army is routed!`);
    }
    return this.winner;
  }

  /** End the active side's turn and start the next side's (healing, fresh move points). */
  endTurn() {
    if (this.winner) return;
    this.history = [];
    this.active = (this.active + 1) % SIDES.length;
    if (this.active === 0) this.turn += 1;
    this.say(`Turn ${this.turn}: ${SIDES[this.active].name} to move.`);
    this.startTurn();
  }

  /** Start-of-turn upkeep for the active side: villages and healers heal, units refresh. */
  startTurn() {
    const mine = this.unitsOf(this.side);
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
      const amount = Math.min(heals.get(u.id) ?? 0, maxHp(u) - u.hp);
      if (amount > 0) {
        u.hp += amount;
        this.say(`${u.side} ${unitType(u).name.toLowerCase()} #${u.id} heals ${amount}.`);
      }
      u.mp = maxMp(u);
      u.acted = false;
    }
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
      log: this.log,
    };
  }

  static fromJSON(data) {
    if (!data || data.version !== SAVE_VERSION) throw new Error("unsupported save version");
    const g = new Game({ map: HexMap.fromJSON(data.map), spawns: data.spawns, villages: data.villages, seed: data.seed });
    g.rng.state = data.rng >>> 0;
    g.units = structuredClone(data.units);
    Object.assign(g, { nextId: data.nextId, turn: data.turn, active: data.active, winner: data.winner, log: structuredClone(data.log) });
    return g;
  }
}
