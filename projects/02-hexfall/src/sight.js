// Line of sight between hexes, used by ranged attacks (and later fog of war).
import { distance, round, key } from "./hex.js";

/**
 * The hexes strictly between `a` and `b` on a straight line, sampled twice with opposite
 * tiny nudges. When the line runs exactly along a hex edge the two samplings pick the
 * hexes on either side, and sight counts as clear if either side is clear (lenient). The
 * nudge (ε, 2ε) in axial coordinates is parallel to no hex diagonal, so every tie is broken,
 * and the same hexes are sampled from either end (symmetric).
 * @returns {Array<Array<{q:number,r:number}>>} two lists of intermediate hexes
 */
export function sightLines(a, b) {
  const n = distance(a, b);
  const lines = [];
  for (const eps of [1e-6, -1e-6]) {
    const pts = [];
    const aq = a.q + eps, ar = a.r + eps * 2;
    const bq = b.q + eps, br = b.r + eps * 2;
    for (let i = 1; i < n; i++) {
      const t = i / n;
      pts.push(round(aq + (bq - aq) * t, ar + (br - ar) * t));
    }
    lines.push(pts);
  }
  return lines;
}

/**
 * Does a viewer at `from` see `to`? Hexes whose terrain blocks sight (forest, village,
 * mountain) block the view unless the viewer stands higher than the blocker — an archer on
 * a hill looks over woods and rooftops, but nobody sees through a mountain.
 * @param {import("./map.js").HexMap} map
 */
export function hasLineOfSight(map, from, to) {
  if (distance(from, to) <= 1) return true;
  const eyeHeight = map.terrainAt(from)?.height ?? 1;
  return sightLines(from, to).some((pts) => pts.every((h) => {
    const t = map.terrainAt(h);
    if (!t) return false;
    if (!t.blocksSight) return true;
    return t.id !== "mountain" && eyeHeight > t.height;
  }));
}

/** Every map hex within `radius` of `from` that it can see (for overlays and fog later). */
export function visibleFrom(map, from, radius) {
  const out = new Set([key(from)]);
  for (const t of map) {
    const d = distance(from, t);
    if (d > 0 && d <= radius && hasLineOfSight(map, from, t)) out.add(key(t));
  }
  return out;
}
