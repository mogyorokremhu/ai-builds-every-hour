// Fog of war: what each side can see. A unit sees every hex within its sight radius that is
// in line of sight (hills add 1, fog/rain/storms take some away); villages a side owns let it
// see their neighbours. Enemies outside what a side sees are hidden from its view, its
// attacks and its AI, and moving next to a hidden enemy springs an ambush.
import { key, spiral, neighbors } from "./hex.js";
import { hasLineOfSight } from "./sight.js";
import { unitType } from "./units.js";
import { currentWeather } from "./weather.js";

export const DEFAULT_SIGHT = 4;

/** Sight radius of `u` standing on `h` in the current weather (at least 1). */
export function sightRadius(game, u, h = u) {
  const base = unitType(u).sight ?? DEFAULT_SIGHT;
  const height = game.map.terrainAt(h)?.height ?? 1;
  return Math.max(1, base + (height >= 2 ? 1 : 0) - currentWeather(game).sightPenalty);
}

/** Hex keys a single viewer at `h` with radius `radius` can see. */
export function viewFrom(map, h, radius) {
  const out = new Set();
  for (const t of spiral(h, radius)) {
    if (map.has(t) && hasLineOfSight(map, h, t)) out.add(key(t));
  }
  return out;
}

/** Every hex key `side` can see right now (its units' views plus around its villages). */
export function visibleHexes(game, side) {
  const out = new Set();
  for (const u of game.units) {
    if (u.side !== side || u.hp <= 0) continue;
    for (const k of viewFrom(game.map, u, sightRadius(game, u))) out.add(k);
  }
  for (const v of game.villages ?? []) {
    if (game.map.get(v)?.owner !== side) continue;
    out.add(key(v));
    for (const n of neighbors(v)) if (game.map.has(n)) out.add(key(n));
  }
  return out;
}

/** Enemy units of `side` it cannot see (empty when `visible` is null = no fog). */
export function hiddenEnemies(game, side, visible) {
  if (!visible) return [];
  return game.units.filter((u) => u.side !== side && u.hp > 0 && !visible.has(key(u)));
}

/**
 * Merge `visible` into the side's explored memory (a Set of keys) and return it. Explored
 * hexes stay drawn (terrain only) after the units that saw them move on.
 */
export function remember(explored, visible) {
  for (const k of visible) explored.add(k);
  return explored;
}
