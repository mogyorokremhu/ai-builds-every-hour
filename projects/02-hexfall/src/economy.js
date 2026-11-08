// Economy and objectives: village ownership, income, recruiting at the keep, battle score.
// Pure functions over a Game-like object ({map, units, villages, spawns, gold, rules, ...}).
import { key } from "./hex.js";
import { unitType, maxHp } from "./units.js";

/** Default battle rules (a Game copies these and lets options override them). */
export const DEFAULT_RULES = Object.freeze({
  startGold: 20,        // gold each side starts with
  baseIncome: 2,        // gold per turn regardless of villages
  villageIncome: 2,     // gold per owned village per turn
  holdShare: 2 / 3,     // share of all villages a side must own to start a hold
  holdTurns: 4,         // ...for this many of its own consecutive turn starts to win
  turnLimit: 30,        // after this many turns the battle is decided on score (0 = no limit)
  villageScore: 12,     // score per owned village at the turn limit
  weather: true,        // seeded weather fronts (rain, fog, storms) from turn 4 on
  fog: false,           // fog of war: sides only see what their units see
});

/** Village hexes owned by `side`. */
export function ownedVillages(game, side) {
  return game.villages.filter((v) => game.map.get(v)?.owner === side);
}

/** Gold `side` collects at the start of its turn. */
export function income(game, side) {
  return game.rules.baseIncome + game.rules.villageIncome * ownedVillages(game, side).length;
}

/** Villages a side must hold for a hold victory (0 = hold victories disabled). */
export function holdTarget(game) {
  const n = game.villages.length;
  if (!n || !game.rules.holdTurns) return 0;
  return Math.max(1, Math.ceil(n * game.rules.holdShare - 1e-9));
}

/**
 * Take a village for `side` if `h` is one. Returns the previous owner (undefined if `h`
 * is not a village or `side` already owns it).
 */
export function capture(game, side, h) {
  const t = game.map.get(h);
  if (!t || t.terrain !== "village" || t.owner === side) return undefined;
  const prev = t.owner;
  t.owner = side;
  return prev;
}

/** The keep hex of side index `i` (first hex of its deployment zone when it is a keep). */
export function keepOf(game, i) {
  const h = game.spawns[i]?.[0];
  return h && game.map.get(h)?.terrain === "keep" ? h : null;
}

/**
 * Hexes where side index `i` may place a recruit: free keep/castle hexes of its deployment
 * zone. Recruiting is impossible while an enemy unit stands on the keep.
 */
export function recruitHexes(game, i) {
  const keep = keepOf(game, i);
  if (!keep) return [];
  const side = game.sideIds[i];
  const onKeep = game.unitAt(keep);
  if (onKeep && onKeep.side !== side) return [];
  return game.spawns[i].filter((h) => {
    const id = game.map.get(h)?.terrain;
    return (id === "keep" || id === "castle") && !game.unitAt(h);
  });
}

/** Why `side` cannot recruit `type` right now ("" = it can). */
export function recruitProblem(game, i, type) {
  const t = unitType(type);
  if (!keepOf(game, i)) return "no keep on this map";
  if (!recruitHexes(game, i).length) {
    const occupant = game.unitAt(keepOf(game, i));
    return occupant && occupant.side !== game.sideIds[i] ? "the enemy holds your keep" : "no free castle hex";
  }
  if (game.gold[i] < t.cost) return `needs ${t.cost} gold`;
  return "";
}

/** Battle score of `side`: army value (cost × health share) + villages + gold. */
export function score(game, side) {
  const i = game.sideIds.indexOf(side);
  let army = 0;
  for (const u of game.units) if (u.side === side && u.hp > 0) army += unitType(u).cost * (u.hp / maxHp(u)) * (1 + 0.25 * (u.level - 1));
  const villages = ownedVillages(game, side).length * game.rules.villageScore;
  return { army: Math.round(army), villages, gold: game.gold[i] ?? 0, total: Math.round(army) + villages + (game.gold[i] ?? 0) };
}

/** Village hex keys → owner, for quick lookups (renderer, AI). */
export function ownerMap(game) {
  const m = new Map();
  for (const v of game.villages) m.set(key(v), game.map.get(v)?.owner ?? null);
  return m;
}
