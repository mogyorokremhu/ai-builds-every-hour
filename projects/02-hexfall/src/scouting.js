// AI scouting under fog of war: when a side sees no enemy it heads for the unexplored frontier.
import { key, neighbors, distance } from "./hex.js";

/**
 * Frontier hexes of `side`: passable hexes it has never seen that touch an explored hex.
 * Sorted by closeness to the enemy keep (or the map centre), at most `limit` returned.
 * Empty without fog.
 */
export function frontier(game, side, limit = 6) {
  if (!game.rules.fog) return [];
  const idx = game.sideIndex(side);
  const explored = game.explored[idx];
  const seen = new Set();
  const out = [];
  for (const k of explored) {
    const [q, r] = k.split(",").map(Number);
    for (const n of neighbors({ q, r })) {
      const nk = key(n);
      if (seen.has(nk) || explored.has(nk) || !game.map.has(n) || !game.map.passable(n)) continue;
      seen.add(nk);
      out.push(n);
    }
  }
  const foeKeep = game.spawns[(idx + 1) % 2]?.[0] ?? { q: Math.floor(game.map.cols / 2), r: Math.floor(game.map.rows / 2) };
  out.sort((a, b) => distance(a, foeKeep) - distance(b, foeKeep) || a.q - b.q || a.r - b.r);
  return out.slice(0, limit);
}

/** Should the AI scout? Fog on and not a single enemy in view. */
export function needsScouting(game, side) {
  if (!game.rules.fog) return false;
  return !game.units.some((u) => u.side !== side && u.hp > 0 && game.isVisible(side, u));
}

/** Goal hexes to add to the AI's distance field while scouting ([] otherwise). */
export function scoutGoals(game, side) {
  return needsScouting(game, side) ? frontier(game, side) : [];
}
