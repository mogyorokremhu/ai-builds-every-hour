// Combat: attack options, damage rules, exact forecasts and seeded resolution.
import { distance, neighbors, key } from "./hex.js";
import { hasLineOfSight } from "./sight.js";
import { todMultiplier } from "./timeofday.js";
import { currentWeather } from "./weather.js";
import { attackMultiplier, defenseMultiplier } from "./status.js";
import {
  meleeAttack, rangedAttack, attackRange, defenseOf, hasTrait, gainXp, unitType,
} from "./units.js";

/** The five equally likely damage rolls (a ±20% spread, seeded). */
export const ROLLS = Object.freeze([0.8, 0.9, 1.0, 1.1, 1.2]);
export const FLANK_BONUS = 0.1;      // per extra ally adjacent to the target (melee)
export const MAX_FLANK = 3;
export const ANTI_CAVALRY = 1.5;
export const XP_FIGHT = 1;           // × enemy level, for surviving an exchange
export const XP_KILL = 8;            // × enemy level

/** Ranged reach of `u` standing on `h`: +1 from high ground (hills), less in fog and storms (min 1). */
export function effectiveRange(game, u, h = u) {
  if (!rangedAttack(u)) return 0;
  const height = game.map.terrainAt(h)?.height ?? 1;
  return Math.max(1, attackRange(u) + (height >= 2 ? 1 : 0) - currentWeather(game).rangePenalty);
}

/**
 * Which attack (if any) `attacker` standing on `from` can use against `target`.
 * At distance 1 the stronger of melee and ranged is used; ranged attacks need range and a
 * clear line of sight.
 * @returns {"melee"|"ranged"|null}
 */
export function attackKind(game, attacker, target, from = attacker) {
  const d = distance(from, target);
  const melee = d === 1 ? meleeAttack(attacker) : 0;
  const ranged = rangedAttack(attacker) && d >= 1 && d <= effectiveRange(game, attacker, from)
    && hasLineOfSight(game.map, from, target) ? rangedAttack(attacker) : 0;
  if (!melee && !ranged) return null;
  return ranged > melee ? "ranged" : "melee";
}

/** Can `defender` (on its own hex) strike back at an attacker on `from` with the same kind? */
export function counterKind(game, defender, from, kind) {
  const d = distance(defender, from);
  if (kind === "melee") return d === 1 && meleeAttack(defender) ? "melee" : null;
  if (!rangedAttack(defender) || d > effectiveRange(game, defender)) return null;
  return hasLineOfSight(game.map, defender, from) ? "ranged" : null;
}

/** Allies of `attacker` (other than itself) adjacent to `target` — they flank it. */
export function flankers(game, attacker, target) {
  const around = new Set(neighbors(target).map(key));
  return game.units.filter((u) => u.side === attacker.side && u.id !== attacker.id && u.hp > 0
    && around.has(key(u))).length;
}

/**
 * Modifiers for one strike, before the random roll.
 * The time of day scales lawful/chaotic attackers (±25%); games without a turn counter count as dawn.
 * Statuses (rallied, slowed, braced), the weather (ranged only) and an ability multiplier `extra`
 * (charge ×1.5, volley ×0.75, ...) are folded into `status`, `weather` and `extra`.
 * @returns {{base:number, flank:number, terrain:number, bonus:number, time:number, status:number,
 *   weather:number, extra:number, multiplier:number, armor:number}}
 */
export function strikeModifiers(game, attacker, defender, kind, extra = 1) {
  const base = kind === "melee" ? meleeAttack(attacker) : rangedAttack(attacker);
  const flank = kind === "melee" ? Math.min(MAX_FLANK, flankers(game, attacker, defender)) * FLANK_BONUS : 0;
  const terrainDef = hasTrait(attacker, "magic") ? 0 : (game.map.terrainAt(defender)?.defense ?? 0);
  const bonus = kind === "melee" && hasTrait(attacker, "antiCavalry") && hasTrait(defender, "mounted") ? ANTI_CAVALRY : 1;
  const time = todMultiplier(unitType(attacker).alignment ?? "neutral", game.turn ?? 1);
  const status = attackMultiplier(attacker) * defenseMultiplier(defender);
  const weather = kind === "ranged" ? currentWeather(game).ranged : 1;
  const multiplier = (1 + flank) * (1 - terrainDef / 100) * bonus * time * status * weather * extra;
  return { base, flank, terrain: terrainDef, bonus, time, status, weather, extra, multiplier, armor: defenseOf(defender) };
}

/** Damage for each of the five rolls (index-aligned with ROLLS); always at least 1. */
export function damageRolls(game, attacker, defender, kind, extra = 1) {
  const m = strikeModifiers(game, attacker, defender, kind, extra);
  return ROLLS.map((roll) => Math.max(1, Math.round(m.base * m.multiplier * roll) - m.armor));
}

const stats = (xs) => ({ min: Math.min(...xs), max: Math.max(...xs), expected: xs.reduce((s, x) => s + x, 0) / xs.length });

/**
 * Exact outcome forecast for `attacker` hitting `target` from hex `from` (default: where
 * it stands). The attack and the counter each pick one of five equally likely rolls, and
 * a target that dies does not strike back — so all 25 outcomes are enumerated.
 * `opts.mult` scales both strikes (a charge doubles the stakes for both sides); `opts.counter`
 * false suppresses the counter-strike.
 * @returns {null | {kind:string, from:object, dealt:{min:number,max:number,expected:number}, counter:string|null,
 *   taken:{min:number,max:number,expected:number}|null, killChance:number, deathChance:number,
 *   expectedDealt:number, expectedTaken:number, flank:number}}
 */
export function forecast(game, attacker, target, from = attacker, opts = {}) {
  const kind = opts.kind ?? attackKind(game, attacker, target, from);
  if (!kind) return null;
  const mult = opts.mult ?? 1;
  const moved = { ...attacker, q: from.q, r: from.r };
  const dealtRolls = damageRolls(game, moved, target, kind, mult);
  const counter = opts.counter === false ? null : counterKind(game, target, from, kind);
  const takenRolls = counter ? damageRolls(game, target, moved, counter, mult) : null;
  let kill = 0, death = 0, dealt = 0, taken = 0;
  for (const d of dealtRolls) {
    const p = 1 / ROLLS.length;
    dealt += p * Math.min(d, target.hp);
    if (d >= target.hp) {
      kill += p;
      continue;
    }
    if (!takenRolls) continue;
    for (const t of takenRolls) {
      const pp = p / ROLLS.length;
      taken += pp * Math.min(t, attacker.hp);
      if (t >= attacker.hp) death += pp;
    }
  }
  return {
    kind, from: { q: from.q, r: from.r }, counter,
    dealt: stats(dealtRolls), taken: takenRolls ? stats(takenRolls) : null,
    killChance: kill, deathChance: death, expectedDealt: dealt, expectedTaken: taken,
    flank: kind === "melee" ? Math.min(MAX_FLANK, flankers(game, attacker, target)) : 0,
  };
}

/**
 * Resolve an attack with the game's seeded RNG: one strike, then (if the target lives and
 * can reach) one counter-strike. Dead units are removed from `game.units`; survivors and
 * killers gain experience and may be promoted.
 * @returns {{kind:string, counter:string|null, dealt:number, taken:number, killed:number[], promotions:Array<{id:number, perks:string[]}>, lines:string[]}}
 */
export function resolveAttack(game, attacker, target, opts = {}) {
  const kind = opts.kind ?? attackKind(game, attacker, target);
  if (!kind) throw new Error(`unit ${attacker.id} cannot attack unit ${target.id}`);
  const mult = opts.mult ?? 1;
  const out = { kind, counter: null, dealt: 0, taken: 0, killed: [], promotions: [], lines: [] };
  const roll = () => game.rng.int(0, ROLLS.length - 1);

  const dealt = Math.min(target.hp, damageRolls(game, attacker, target, kind, mult)[roll()]);
  target.hp -= dealt;
  out.dealt = dealt;
  const verb = opts.verb ?? (kind === "melee" ? "hits" : hasTrait(attacker, "magic") ? "blasts" : "shoots");
  out.lines.push(`${name(attacker)} ${verb} ${name(target)} for ${dealt}${target.hp <= 0 ? " — killed!" : ` (${target.hp} HP left)`}`);

  if (target.hp > 0 && opts.counter !== false) {
    out.counter = counterKind(game, target, attacker, kind);
    if (out.counter) {
      const taken = Math.min(attacker.hp, damageRolls(game, target, attacker, out.counter, mult)[roll()]);
      attacker.hp -= taken;
      out.taken = taken;
      out.lines.push(`${name(target)} strikes back for ${taken}${attacker.hp <= 0 ? " — killed!" : ""}`);
    }
  }

  for (const [u, foe] of [[attacker, target], [target, attacker]]) award(u, foe, out);
  for (const u of [target, attacker]) if (u.hp <= 0) out.killed.push(u.id);
  if (out.killed.length) game.units = game.units.filter((u) => u.hp > 0);
  return out;
}

/** Log name of a unit: "red archer #3". */
export const name = (u) => `${u.side} ${unitType(u).name.toLowerCase()} #${u.id}`;

/**
 * Experience for `u` after an exchange with `foe` (a kill is worth much more). Promotions are
 * recorded on `out` ({promotions, lines}). Dead units and fights between allies earn nothing.
 */
export function award(u, foe, out) {
  if (u.hp <= 0 || u.side === foe.side) return;
  const xp = foe.hp <= 0 ? XP_KILL * foe.level : XP_FIGHT * foe.level;
  if (foe.hp <= 0) u.kills += 1;
  const perks = gainXp(u, xp);
  if (perks.length) {
    out.promotions.push({ id: u.id, perks });
    out.lines.push(`${name(u)} is promoted: ${perks.join(", ")}!`);
  }
}
