// Unit abilities: special actions that replace a unit's attack for the turn. Each ability has
// a target rule, an exact or expected-value preview (for the UI and the AI) and a seeded
// resolution. Cooldowns are stored on the unit as {id: turnsLeft} and tick at its turn start.
//
//   charge     cavalry  — melee after moving this turn: ×1.5 damage both ways
//   volley     archer   — 75% shot at the target and every enemy next to it; slows the target; no counter
//   fireball   mage     — blast on a hex in range: full damage there, 60% on the ring (friends too!);
//                         dry plains and forests catch fire
//   heal       healer   — restore 12 HP (+medic bonus) to an adjacent ally and cure poison
//   shieldwall spearman — the spearman and adjacent allies are braced (−35% damage) until its next turn
//   rally      swordsman— the swordsman and adjacent allies are rallied (+20% damage) this turn and next
//   envenom    rogue    — melee strike that poisons a surviving target for 3 turns
import { key, distance, neighbors } from "./hex.js";
import { hasLineOfSight } from "./sight.js";
import {
  attackKind, counterKind, damageRolls, forecast, effectiveRange, award, name, ROLLS,
} from "./combat.js";
import { unitType, maxHp, healAmount } from "./units.js";
import { addStatus, removeStatus, hasStatus } from "./status.js";
import { FLAMMABLE } from "./terrain.js";
import { currentWeather } from "./weather.js";

export const CHARGE_MULT = 1.5;
export const VOLLEY_MULT = 0.75;
export const FIREBALL_RING = 0.6;
export const FIRE_TURNS = 3;
export const HEAL_BASE = 12;
export const POISON_TURNS = 3;

/**
 * @typedef {object} Ability
 * @property {string} id
 * @property {string} name
 * @property {string} icon
 * @property {number} cooldown   own turns before it can be used again (0 = every turn)
 * @property {"enemy"|"ally"|"hex"|"self"} target
 * @property {string} text
 */

/** @type {Record<string, Ability>} */
export const ABILITIES = Object.freeze({
  charge: { id: "charge", name: "Charge", icon: "🐎", cooldown: 2, target: "enemy", text: "Melee attack after moving this turn: both sides deal ×1.5 damage." },
  volley: { id: "volley", name: "Volley", icon: "🏹", cooldown: 3, target: "enemy", text: "Arrows rain on the target and every enemy next to it (75% damage). Slows the target. No counter." },
  fireball: { id: "fireball", name: "Fireball", icon: "🔥", cooldown: 3, target: "hex", text: "Blast a hex in range: full damage there, 60% on the six around it — allies included. Dry plains and forests catch fire. No counter." },
  heal: { id: "heal", name: "Heal", icon: "✚", cooldown: 0, target: "ally", text: "Restore 12 HP (medics more) to an adjacent ally and cure its poison." },
  shieldwall: { id: "shieldwall", name: "Shield wall", icon: "🛡", cooldown: 3, target: "self", text: "This spearman and adjacent allies take 35% less damage until its next turn." },
  rally: { id: "rally", name: "Rally", icon: "⚑", cooldown: 3, target: "self", text: "This swordsman and adjacent allies deal 20% more damage this turn and next." },
  envenom: { id: "envenom", name: "Envenom", icon: "☠", cooldown: 2, target: "enemy", text: "Melee strike that poisons a surviving target for 3 turns." },
});

/** Abilities of a unit (by type). */
export function abilitiesOf(u) {
  return unitType(u).abilities ?? [];
}

/** Turns left before `u` can use `id` again (0 = ready). */
export function cooldownLeft(u, id) {
  return u.cd?.[id] ?? 0;
}

/** Count down every cooldown of `u` by one (start of its own turn). */
export function tickCooldowns(u) {
  if (!u.cd) return;
  for (const [id, n] of Object.entries(u.cd)) {
    if (n <= 1) delete u.cd[id];
    else u.cd[id] = n - 1;
  }
}

const visibleTo = (game, side) => (typeof game.isVisible === "function" ? (u) => game.isVisible(side, u) : () => true);

/**
 * Why `u` cannot use ability `id` from hex `from` at all ("" = it can, given a target).
 * `from` defaults to where it stands; `moved` (default `u.moved`) says if it moved this turn.
 */
export function abilityProblem(game, u, id, { moved = u.moved } = {}) {
  if (!abilitiesOf(u).includes(id)) return "not this unit's ability";
  if (game.winner) return "the battle is over";
  if (u.side !== game.side) return "not this unit's turn";
  if (u.acted) return "already acted this turn";
  const left = cooldownLeft(u, id);
  if (left > 0) return `recharging (${left} turn${left === 1 ? "" : "s"})`;
  if (id === "charge" && !moved) return "move first to build up speed";
  return "";
}

/** Units within one hex of `h` (the blast or the shield-wall ring), alive. */
function around(game, h, includeCentre = true) {
  const ks = new Set(neighbors(h).map(key));
  if (includeCentre) ks.add(key(h));
  return game.units.filter((u) => u.hp > 0 && ks.has(key(u)));
}

/**
 * Valid targets of ability `id` for `u` standing on `from` (default: its hex), as hexes.
 * Charge/envenom need a melee target, volley a ranged one in sight, fireball any hex in range and
 * sight, heal a hurt or poisoned adjacent ally, shield wall / rally the unit's own hex.
 * @returns {Array<{q:number,r:number}>}
 */
export function abilityTargets(game, u, id, from = u, opts = {}) {
  if (abilityProblem(game, u, id, opts)) return [];
  const seen = visibleTo(game, u.side);
  const enemies = game.units.filter((t) => t.side !== u.side && t.hp > 0 && seen(t));
  const at = { ...u, q: from.q, r: from.r };
  switch (id) {
    case "charge":
    case "envenom":
      return enemies.filter((t) => distance(from, t) === 1 && attackKind(game, at, t, from) === "melee").map(hexOf);
    case "volley":
      return enemies.filter((t) => attackKind(game, at, t, from) === "ranged").map(hexOf);
    case "fireball": {
      const reach = effectiveRange(game, at, from);
      const out = [];
      for (const t of game.map) {
        const d = distance(from, t);
        if (d >= 1 && d <= reach && hasLineOfSight(game.map, from, t)) out.push(hexOf(t));
      }
      return out;
    }
    case "heal":
      return game.units.filter((a) => a.side === u.side && a.id !== u.id && a.hp > 0 && distance(from, a) === 1
        && (a.hp < maxHp(a) || hasStatus(a, "poisoned"))).map(hexOf);
    case "shieldwall":
    case "rally":
      return [hexOf(from)];
    default:
      return [];
  }
}

const hexOf = (h) => ({ q: h.q, r: h.r });
const mean = (xs) => xs.reduce((s, x) => s + x, 0) / xs.length;

/**
 * What using ability `id` from `from` on `target` would do, in expected values (no RNG used).
 * Damage abilities list every unit hit with its expected damage and kill chance; support
 * abilities list who is helped. The AI turns this into a score; the UI shows it as a tooltip.
 * @returns {null | {id:string, hits:Array<{unit:object, expected:number, killChance:number, min:number, max:number}>,
 *   counter:{expected:number, deathChance:number}|null, heal:number, cures:number, buffs:object[], fires:number}}
 */
export function abilityPreview(game, u, id, target, from = u, opts = {}) {
  const valid = abilityTargets(game, u, id, from, opts);
  if (!valid.some((h) => h.q === target.q && h.r === target.r)) return null;
  const at = { ...u, q: from.q, r: from.r };
  const out = { id, hits: [], counter: null, heal: 0, cures: 0, buffs: [], fires: 0 };
  const hit = (victim, rolls) => {
    out.hits.push({
      unit: victim, min: Math.min(...rolls), max: Math.max(...rolls),
      expected: mean(rolls.map((d) => Math.min(d, victim.hp))),
      killChance: rolls.filter((d) => d >= victim.hp).length / rolls.length,
    });
  };
  const victim = game.unitAt(target);
  switch (id) {
    case "charge":
    case "envenom": {
      const f = forecast(game, at, victim, from, { kind: "melee", mult: id === "charge" ? CHARGE_MULT : 1 });
      hit(victim, damageRolls(game, at, victim, "melee", id === "charge" ? CHARGE_MULT : 1));
      out.counter = f.counter ? { expected: f.expectedTaken, deathChance: f.deathChance } : null;
      break;
    }
    case "volley": {
      hit(victim, damageRolls(game, at, victim, "ranged", VOLLEY_MULT));
      for (const n of around(game, victim, false)) if (n.side !== u.side) hit(n, damageRolls(game, at, n, "ranged", VOLLEY_MULT));
      break;
    }
    case "fireball": {
      for (const n of around(game, target)) {
        const mult = key(n) === key(target) ? 1 : FIREBALL_RING;
        hit(n, damageRolls(game, at, n, "ranged", mult));
      }
      if (!currentWeather(game).wet) {
        for (const h of [target, ...neighbors(target)]) {
          const t = game.map.get(h);
          if (t && FLAMMABLE.has(t.terrain) && !(t.fire > 0) && key(h) !== key(from)) out.fires += 1;
        }
      }
      break;
    }
    case "heal": {
      out.heal = Math.min(HEAL_BASE + healBonus(u), maxHp(victim) - victim.hp);
      out.cures = hasStatus(victim, "poisoned") ? 1 : 0;
      out.buffs.push(victim);
      break;
    }
    case "shieldwall":
    case "rally":
      for (const a of around(game, from)) if (a.side === u.side) out.buffs.push(key(a) === key(from) ? u : a);
      if (!out.buffs.includes(u)) out.buffs.push(u);
      break;
    default:
      return null;
  }
  return out;
}

/** Extra healing from the medic perk (heal amount beyond the base 4 of the passive heal). */
function healBonus(u) {
  return Math.max(0, healAmount(u) - 4);
}

/**
 * Use ability `id` of `u` on `target` (a hex). Applies damage with the game's seeded RNG,
 * statuses, fires, healing and experience; the unit's action for the turn is spent and the
 * ability starts its cooldown. Returns {id, lines, killed, promotions, hits}.
 */
export function useAbility(game, u, id, target) {
  const problem = abilityProblem(game, u, id);
  if (problem) throw new Error(`${unitType(u).name} cannot use ${id}: ${problem}`);
  if (!abilityTargets(game, u, id).some((h) => h.q === target.q && h.r === target.r)) {
    throw new Error(`invalid ${id} target ${key(target)}`);
  }
  const out = { id, lines: [], killed: [], promotions: [], hits: [] };
  const roll = () => game.rng.int(0, ROLLS.length - 1);
  const strike = (victim, kind, mult) => {
    const dmg = Math.min(victim.hp, damageRolls(game, u, victim, kind, mult)[roll()]);
    victim.hp -= dmg;
    out.hits.push({ id: victim.id, damage: dmg });
    return dmg;
  };
  const ab = ABILITIES[id];
  const victim = game.unitAt(target);
  switch (id) {
    case "charge":
    case "envenom": {
      const mult = id === "charge" ? CHARGE_MULT : 1;
      const dealt = strike(victim, "melee", mult);
      out.lines.push(`${name(u)} ${id === "charge" ? "charges" : "stabs"} ${name(victim)} for ${dealt}${victim.hp <= 0 ? " — killed!" : ` (${victim.hp} HP left)`}`);
      if (victim.hp > 0 && id === "envenom") {
        addStatus(victim, "poisoned", POISON_TURNS);
        out.lines.push(`${name(victim)} is poisoned!`);
      }
      if (victim.hp > 0 && counterKind(game, victim, u, "melee")) {
        const taken = Math.min(u.hp, damageRolls(game, victim, u, "melee", mult)[roll()]);
        u.hp -= taken;
        out.lines.push(`${name(victim)} strikes back for ${taken}${u.hp <= 0 ? " — killed!" : ""}`);
      }
      award(u, victim, out);
      award(victim, u, out);
      break;
    }
    case "volley": {
      const victims = [victim, ...around(game, victim, false).filter((n) => n.side !== u.side)];
      const parts = victims.map((v) => `${name(v)} ${strike(v, "ranged", VOLLEY_MULT)}${v.hp <= 0 ? " (killed)" : ""}`);
      out.lines.push(`${name(u)} looses a volley: ${parts.join(", ")}`);
      if (victim.hp > 0) addStatus(victim, "slowed", 1);
      for (const v of victims) award(u, v, out);
      break;
    }
    case "fireball": {
      const victims = around(game, target);
      const parts = victims.map((v) => `${name(v)} ${strike(v, "ranged", key(v) === key(target) ? 1 : FIREBALL_RING)}${v.hp <= 0 ? " (killed)" : ""}`);
      out.lines.push(`${name(u)} hurls a fireball${parts.length ? `: ${parts.join(", ")}` : " at empty ground"}`);
      if (!currentWeather(game).wet) {
        let lit = 0;
        for (const h of [target, ...neighbors(target)]) {
          const t = game.map.get(h);
          if (t && FLAMMABLE.has(t.terrain) && !(t.fire > 0) && key(h) !== key(u)) {
            t.fire = FIRE_TURNS;
            lit += 1;
          }
        }
        if (lit) out.lines.push(`${lit} hex${lit === 1 ? "" : "es"} catch fire!`);
      }
      for (const v of victims) award(u, v, out);
      break;
    }
    case "heal": {
      const amount = Math.min(HEAL_BASE + healBonus(u), maxHp(victim) - victim.hp);
      victim.hp += amount;
      const cured = hasStatus(victim, "poisoned");
      removeStatus(victim, "poisoned");
      out.lines.push(`${name(u)} heals ${name(victim)} for ${amount}${cured ? " and cures its poison" : ""}`);
      break;
    }
    case "shieldwall":
    case "rally": {
      const status = id === "shieldwall" ? "braced" : "rallied";
      const allies = [u, ...around(game, u, false).filter((a) => a.side === u.side)];
      for (const a of allies) addStatus(a, status, id === "shieldwall" ? 1 : 2);
      out.lines.push(`${name(u)} ${id === "shieldwall" ? "forms a shield wall" : "rallies the line"} (${allies.length} unit${allies.length === 1 ? "" : "s"})`);
      break;
    }
    default:
      throw new Error(`unknown ability ${id}`);
  }
  if (ab.cooldown) (u.cd ??= {})[id] = ab.cooldown; // ticks at our turn starts: back after `cooldown` turns
  u.acted = true;
  u.mp = 0;
  for (const v of game.units) if (v.hp <= 0) out.killed.push(v.id);
  if (out.killed.length) game.units = game.units.filter((v) => v.hp > 0);
  return out;
}

/** Short "ready" / "2 turns" label for buttons. */
export function abilityStatus(game, u, id) {
  const problem = abilityProblem(game, u, id);
  return problem || (abilityTargets(game, u, id).length ? "ready" : "no target in reach");
}
