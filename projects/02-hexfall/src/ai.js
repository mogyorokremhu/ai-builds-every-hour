// Utility AI: every option (recruit, move, move+attack, ability, hold) gets a score from a few
// weighted considerations — damage traded in gold value, kill chances, the threat waiting
// at the destination, terrain, villages, healing and progress towards goals — and the best
// one is played, one action at a time. Deterministic for a given seed.
import { key, distance, neighbors } from "./hex.js";
import { RNG } from "./rng.js";
import { destinations } from "./movement.js";
import { forecast, effectiveRange } from "./combat.js";
import { unitType, maxHp, defenseOf, hasTrait, healAmount, RECRUITABLE, UNIT_TYPES } from "./units.js";
import { threatMap, distanceField } from "./influence.js";
import { alignmentBonus, timeOfDay } from "./timeofday.js";
import { ABILITIES, abilitiesOf, abilityTargets, abilityPreview, POISON_TURNS } from "./abilities.js";
import { POISON_DAMAGE } from "./status.js";
import { scoutGoals } from "./scouting.js";

/**
 * Difficulty presets.
 * - noise: random jitter added to every option's score (bigger = sloppier)
 * - risk: how much expected losses weigh against gains (1 = fully)
 * - focus: bonus weight on kill chances (finishing wounded units)
 * - recruit: share of the treasury the AI is willing to spend each turn
 */
export const DIFFICULTY = Object.freeze({
  easy: { noise: 6, risk: 0.45, focus: 0.6, recruit: 0.6, label: "Easy" },
  normal: { noise: 1.5, risk: 0.8, focus: 1, recruit: 1, label: "Normal" },
  hard: { noise: 0, risk: 1, focus: 1.3, recruit: 1, label: "Hard" },
});

/** Preferred army mix (relative weights) before counter-picking adjustments. */
export const RECRUIT_MIX = Object.freeze({
  swordsman: 3, spearman: 2.2, archer: 2.2, cavalry: 2, mage: 1.4, healer: 1, rogue: 1.4,
});

const valueRate = (u) => unitType(u).cost / maxHp(u);

export class AIPlayer {
  /**
   * @param {string} side  side id it plays ("red" / "blue")
   * @param {object} [opts] {difficulty: "easy"|"normal"|"hard", seed}
   */
  constructor(side, { difficulty = "normal", seed = 1 } = {}) {
    if (!DIFFICULTY[difficulty]) throw new Error(`unknown difficulty ${difficulty}`);
    this.side = side;
    this.difficulty = difficulty;
    this.cfg = DIFFICULTY[difficulty];
    this.rng = new RNG((seed ^ 0x9e3779b9) >>> 0);
    this.done = new Set();
    this.turnKey = "";
    this.spent = 0;
  }

  /** Reset per-turn memory when a new turn of ours begins. */
  sync(game) {
    const k = `${game.turn}:${game.active}`;
    if (k !== this.turnKey) {
      this.turnKey = k;
      this.done.clear();
      this.spent = 0;
      this.budget = Math.floor(game.gold[game.active] * this.cfg.recruit);
    }
  }

  /**
   * The next action for this side, without applying it:
   * {type:"recruit", unitType, at} | {type:"attack", unitId, targetId, from} |
   * {type:"move", unitId, to} | {type:"ability", unitId, ability, target, from} |
   * {type:"hold", unitId} | {type:"end"}
   * Each action also carries `score` and a short `why` for debugging.
   */
  nextAction(game) {
    if (game.winner || game.side !== this.side) return { type: "end", why: "not our turn" };
    this.sync(game);
    const recruit = this.chooseRecruit(game);
    if (recruit) return recruit;
    const ctx = this.context(game);
    let best = null;
    for (const u of game.unitsOf(this.side)) {
      if (this.done.has(u.id) || u.acted) continue;
      const opt = this.bestOption(game, u, ctx);
      if (opt && (!best || opt.score > best.score)) best = opt;
    }
    return best ?? { type: "end", why: "every unit has acted" };
  }

  /** Apply an action from nextAction() to `game`. Returns the attack result for attacks. */
  play(game, action) {
    switch (action.type) {
      case "recruit":
        this.spent += unitType(action.unitType).cost;
        return game.recruit(action.unitType, action.at);
      case "move": {
        const u = game.unitById(action.unitId);
        this.done.add(u.id);
        return game.move(u, action.to);
      }
      case "attack": {
        const u = game.unitById(action.unitId);
        const t = game.unitById(action.targetId);
        this.done.add(u.id);
        if (key(action.from) !== key(u)) game.move(u, action.from);
        return game.attack(u, t);
      }
      case "ability": {
        const u = game.unitById(action.unitId);
        this.done.add(u.id);
        if (key(action.from) !== key(u)) game.move(u, action.from);
        // an ambush may have stopped the move short: then the ability may no longer fit
        if (key(action.from) !== key(u) || !game.abilityTargets(u, action.ability).some((h) => key(h) === key(action.target))) return null;
        return game.useAbility(u, action.ability, action.target);
      }
      case "hold":
        this.done.add(action.unitId);
        return null;
      case "end":
        if (!game.winner && game.side === this.side) game.endTurn();
        return null;
      default:
        throw new Error(`unknown action ${action.type}`);
    }
  }

  /** Play a whole turn for this side. Returns the actions taken (the last is "end"). */
  playTurn(game, maxActions = 200) {
    const actions = [];
    for (let i = 0; i < maxActions; i++) {
      const a = this.nextAction(game);
      actions.push(a);
      this.play(game, a);
      if (a.type === "end" || game.winner) break;
    }
    if (!game.winner && game.side === this.side) game.endTurn();
    return actions;
  }

  // ------------------------------------------------------------ recruiting

  /** Pick a unit type to recruit (counter-picking the enemy army), or null. */
  chooseRecruit(game) {
    if (!game.recruitHexes().length) return null;
    const mine = game.unitsOf(this.side);
    const foes = game.units.filter((u) => u.side !== this.side && (!game.isVisible || game.isVisible(this.side, u)));
    const count = (list, pred) => list.filter(pred).length;
    const mounted = count(foes, (u) => hasTrait(u, "mounted"));
    const ranged = count(foes, (u) => unitType(u).ranged > 0);
    const healers = count(mine, (u) => hasTrait(u, "healer"));
    const soon = timeOfDay(game.turn + 2);
    const options = [];
    for (const type of RECRUITABLE) {
      const t = UNIT_TYPES[type];
      let w = RECRUIT_MIX[type] ?? 1;
      w /= 1 + count(mine, (u) => u.type === type) * 0.6;
      if (type === "spearman") w *= 1 + mounted * 0.2;
      if (type === "cavalry") w *= 1 + ranged * 0.25;
      if (type === "healer" && (healers >= 1 || mine.length < 4)) w *= 0.2;
      w *= 1 + alignmentBonus(t.alignment, soon) / 100;
      options.push([type, w * (0.85 + this.rng.next() * 0.3)]);
    }
    options.sort((a, b) => b[1] - a[1]);
    const affordable = ([type]) => !game.recruitProblem(type) && this.spent + UNIT_TYPES[type].cost <= Math.max(this.budget, UNIT_TYPES[type].cost);
    // Save up for the unit we want most, unless the army is thin (then take the best we can pay for).
    const pick = options.find(affordable);
    if (!pick) return null;
    if (pick !== options[0] && mine.length >= 4 && foes.length <= mine.length + 1) return null;
    const type = pick[0];
    const foeKeep = game.spawns[(game.active + 1) % 2]?.[0];
    const hexes = game.recruitHexes().slice()
      .sort((a, b) => (foeKeep ? distance(a, foeKeep) - distance(b, foeKeep) : 0));
    return { type: "recruit", unitType: type, at: hexes[0], score: 100, why: `recruit ${type}` };
  }

  // ------------------------------------------------------------ moving and fighting

  /**
   * Per-decision shared data: threat map, distance fields to goals, endgame state and the
   * villages that need guarding. Under fog of war only the enemies this side sees count.
   * While no enemy is in view the unexplored frontier becomes a goal (scouting).
   */
  context(game) {
    const seen = (u) => !game.isVisible || game.isVisible(this.side, u);
    const threat = threatMap(game, this.side, seen);
    const foes = game.units.filter((u) => u.side !== this.side && u.hp > 0 && seen(u));
    const villagesToTake = game.villages.filter((v) => game.map.get(v)?.owner !== this.side);
    const foeKeep = game.spawns[(game.active + 1) % 2]?.[0];
    const scouts = scoutGoals(game, this.side);
    const goals = [...foes, ...villagesToTake, ...scouts, ...(foeKeep && !scouts.length ? [foeKeep] : [])];
    const safe = [
      ...game.villages.filter((v) => game.map.get(v)?.owner === this.side || !game.map.get(v)?.owner),
      ...game.unitsOf(this.side).filter((u) => hasTrait(u, "healer")).flatMap((u) => neighbors(u)),
    ];
    const ownKeep = game.spawns[game.active]?.[0];
    const keepThreat = ownKeep ? foes.filter((u) => distance(u, ownKeep) <= 3).length : 0;
    // endgame: within 3 turns of the limit, play for points (protect a lead, chase villages when behind)
    const limit = game.rules?.turnLimit ?? 0;
    const turnsLeft = limit ? limit - game.turn : Infinity;
    let lead = 0;
    if (limit && typeof game.score === "function") {
      const other = game.sideIds.find((id) => id !== this.side);
      lead = game.score(this.side).total - game.score(other).total;
    }
    // an enemy that has started a village hold must be broken: its villages are worth more
    const foeIndex = (game.active + 1) % 2;
    const foeHolding = (game.hold?.[foeIndex] ?? 0) > 0;
    // own villages with an enemy close by want a guard standing on them
    const guard = new Set(game.villages.filter((v) => game.map.get(v)?.owner === this.side
      && foes.some((f) => distance(f, v) <= 5)).map(key));
    return {
      threat, foes, endgame: turnsLeft <= 3, turnsLeft, lead, foeHolding, guard,
      goalField: distanceField(game, goals.length ? goals : game.units),
      safeField: distanceField(game, safe.length ? safe : game.villages),
      ownKeep, keepThreat,
    };
  }

  /** The best option for one unit, as an action with a score. */
  bestOption(game, u, ctx) {
    const area = game.area(u);
    let best = null;
    const consider = (cand) => {
      cand.score += this.cfg.noise ? (this.rng.next() - 0.5) * this.cfg.noise : 0;
      if (!best || cand.score > best.score) best = cand;
    };
    for (const node of destinations(area)) {
      const h = node.hex;
      const pos = this.positionScore(game, u, h, ctx);
      const stay = key(h) === key(u);
      consider(stay ? { type: "hold", unitId: u.id, score: pos, why: "hold" }
        : { type: "move", unitId: u.id, to: h, score: pos, why: "move" });
      const reach = effectiveRange(game, u, h) || 1;
      for (const t of ctx.foes) {
        if (distance(h, t) > Math.max(1, reach + 1)) continue;
        const f = forecast(game, u, t, h);
        if (!f) continue;
        const atk = this.attackScore(u, t, f);
        consider({ type: "attack", unitId: u.id, targetId: t.id, from: h, score: atk + pos * 0.6, why: `attack #${t.id} (${Math.round(f.killChance * 100)}% kill)` });
      }
      for (const id of abilitiesOf(u)) {
        const opts = { moved: u.moved || !stay };
        let targets = abilityTargets(game, u, id, h, opts);
        if (id === "fireball") targets = targets.filter((t) => ctx.foes.some((f) => distance(f, t) <= 1));
        for (const target of targets) {
          const p = abilityPreview(game, u, id, target, h, opts);
          if (!p) continue;
          const sc = this.abilityScore(game, u, h, p, ctx);
          if (sc <= 0) continue;
          consider({ type: "ability", unitId: u.id, ability: id, target, from: h, score: sc + pos * 0.6, why: `${id} at ${key(target)}` });
        }
      }
    }
    return best;
  }

  /** Value of an ability preview in the same gold-trade units as attackScore. */
  abilityScore(game, u, h, p, ctx) {
    const risk = this.cfg.risk;
    let s = 0;
    for (const hit of p.hits) {
      const t = hit.unit;
      const value = hit.expected * valueRate(t) + hit.killChance * unitType(t).cost * 0.8 * (1 + 0.3 * (t.level - 1));
      if (t.side === this.side) s -= value * 1.5;          // friendly fire
      else s += value * (hit.killChance > 0 ? this.cfg.focus : 1);
    }
    if (p.counter) {
      s -= p.counter.expected * valueRate(u) * risk + p.counter.deathChance * unitType(u).cost * risk;
    }
    const target = p.hits[0]?.unit;
    if (p.id === "volley" && target && target.side !== this.side) s += 1.5;
    if (p.id === "envenom" && target && p.hits[0].killChance < 1) s += Math.min(target.hp - 1, POISON_DAMAGE * POISON_TURNS) * valueRate(target) * 0.5;
    // burning ground only matters where enemies stand next turn
    if (p.id === "fireball") s += p.fires * 0.1;
    if (p.id === "heal") {
      const a = p.buffs[0];
      s += p.heal * valueRate(a) * 1.3 + p.cures * POISON_DAMAGE * 2 * valueRate(a);
    }
    if (p.id === "shieldwall") {
      for (const a of p.buffs) {
        const th = ctx.threat.get(key(a === u ? h : a));
        if (th) s += Math.min(a.hp, th.damage * 0.75) * 0.35 * valueRate(a) * risk;
      }
    }
    if (p.id === "rally") {
      for (const a of p.buffs) {
        if (a === u || a.acted) continue;
        if (ctx.foes.some((f) => distance(f, a) <= Math.max(2, effectiveRange(game, a) + 1))) s += 2.5;
      }
    }
    // cooldown abilities must be clearly worth spending: an ordinary attack is always there
    const cost = ABILITIES[p.id].cooldown ? 1.5 : 0.5;
    return s > cost ? 3 + s - cost : 0;
  }

  /** Gold-value trade of an attack: damage and kills dealt minus expected losses. */
  attackScore(u, t, f) {
    const risk = this.cfg.risk;
    const gain = f.expectedDealt * valueRate(t) + f.killChance * unitType(t).cost * 0.8 * this.cfg.focus * (1 + 0.3 * (t.level - 1));
    const loss = f.expectedTaken * valueRate(u) * risk + f.deathChance * unitType(u).cost * risk * (1 + 0.3 * (u.level - 1));
    const finishing = t.hp <= maxHp(t) * 0.35 ? 2 * this.cfg.focus : 0;
    return 3 + gain - loss + finishing;
  }

  /** How good it is for `u` to end its move on `h`. */
  positionScore(game, u, h, ctx) {
    const tile = game.map.get(h);
    const ter = game.map.terrainAt(h);
    const hpFrac = u.hp / maxHp(u);
    const wounded = hpFrac < 0.5;
    let s = ter.defense * 0.06;
    if (tile.terrain === "village") {
      let grab = tile.owner !== this.side ? 6 + (tile.owner ? 3 : 0) : 0;
      if (grab && tile.owner && ctx.foeHolding) grab += 6;             // break the enemy's hold
      if (grab && ctx.endgame) grab *= ctx.lead < 0 ? 2 : 1.3;         // points decide the battle soon
      s += grab;
      if (tile.owner === this.side && ctx.guard.has(key(h))) s += 5;   // guard a village raiders can reach
      if (hpFrac < 0.75) s += (1 - hpFrac) * 14;
    }
    if (wounded) {
      for (const n of neighbors(h)) {
        const ally = game.unitAt(n);
        if (ally && ally.side === this.side && ally.id !== u.id && healAmount(ally)) s += (1 - hpFrac) * 8;
      }
    }
    if (healAmount(u)) {
      for (const n of neighbors(h)) {
        const ally = game.unitAt(n);
        if (ally && ally.side === this.side && ally.id !== u.id) s += (1 - ally.hp / maxHp(ally)) * 4;
      }
    }
    // threat: expected incoming damage on this hex, as gold value at risk
    const th = ctx.threat.get(key(h));
    if (th) {
      // a side that leads near the end plays safe: losses now cost the points it would win on
      const caution = ctx.endgame && ctx.lead > 0 ? 1.6 : 1;
      const per = Math.max(1, (th.damage / th.count) * (1 - ter.defense / 100) - defenseOf(u));
      const incoming = Math.min(u.hp, per * th.count * 0.75);
      s -= incoming * valueRate(u) * this.cfg.risk * (wounded ? 1.4 : 0.7) * caution;
      if (incoming >= u.hp) s -= unitType(u).cost * 0.35 * this.cfg.risk * caution;
    }
    if (tile.fire > 0) s -= 4;
    // guard the keep when enemies close in
    if (ctx.ownKeep && ctx.keepThreat && key(h) === key(ctx.ownKeep)) s += 4 + 2 * ctx.keepThreat;
    // progress: weak units fall back to healing spots, the rest push towards goals
    if (hpFrac < 0.35) s -= (ctx.safeField.get(key(h)) ?? 30) * 0.5;
    else s -= (ctx.goalField.get(key(h)) ?? 30) * 0.45;
    return s;
  }
}

/** Convenience: build a pair of AI players for a self-play match. */
export function aiPair(difficulties = ["normal", "normal"], seed = 1) {
  return [new AIPlayer("red", { difficulty: difficulties[0], seed }), new AIPlayer("blue", { difficulty: difficulties[1], seed: seed + 1 })];
}
