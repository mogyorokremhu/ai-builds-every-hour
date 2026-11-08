// Procedural battle maps: noise terrain, guaranteed-connected battlefield, spawns,
// villages and roads. Same seed + options => same map.
import { HexMap } from "./map.js";
import { ValueNoise } from "./noise.js";
import { RNG } from "./rng.js";
import { key, fromKey, distance, toPixel, spiral, fromOffset, toOffset } from "./hex.js";
import { findPath, floodFill } from "./pathfind.js";
import { terrain } from "./terrain.js";

export const DEFAULTS = Object.freeze({
  cols: 24,
  rows: 16,
  seed: 1,
  scale: 0.16,        // noise frequency (smaller = bigger features)
  water: 0.3,         // elevation below this is deep water
  villages: 6,
  spawnSize: 6,       // hexes per side's deployment zone
  roads: true,
  symmetric: false,   // point-mirrored map (fair for competitive play)
  rivers: 2,          // rivers flowing downhill from the high ground
});

const RIVER_STOP = new Set(["water", "shallows", "river"]);

/**
 * Carve a river from `source` downhill: each step goes to the lowest unvisited neighbour
 * (it may cut through small rises, up to +0.08 elevation) until it reaches open water,
 * another river or the map edge. A river stuck in a deeper hollow pools into shallows.
 * Returns the river hexes.
 */
export function carveRiver(map, source, maxLength = 60) {
  const out = [];
  const seen = new Set();
  let cur = source;
  for (let i = 0; i < maxLength; i++) {
    const t = map.get(cur);
    if (!t || RIVER_STOP.has(t.terrain) && i > 0) break;
    out.push(cur);
    seen.add(key(cur));
    const ns = map.neighbors(cur).filter((n) => !seen.has(key(n)));
    if (map.neighbors(cur).length < 6 && i > 0) break; // reached the edge of the map
    if (!ns.length) break;
    ns.sort((a, b) => map.get(a).elevation - map.get(b).elevation);
    const next = ns[0];
    if (map.get(next).elevation > t.elevation + 0.08 && !RIVER_STOP.has(map.get(next).terrain)) {
      // a hollow: pool into a small lake and stop
      for (const n of map.neighbors(cur)) if (map.get(n).terrain !== "mountain" && !seen.has(key(n))) map.get(n).terrain = "shallows";
      break;
    }
    cur = next;
  }
  for (const h of out) map.get(h).terrain = "river";
  return out;
}

function riverSources(map, count, rng) {
  const high = [...map].filter((t) => t.terrain === "hills" || t.terrain === "mountain")
    .sort((a, b) => b.elevation - a.elevation);
  const out = [];
  for (const t of high) {
    if (out.length >= count) break;
    if (out.some((s) => distance(s, t) < 6)) continue;
    if (rng.chance(0.75)) out.push({ q: t.q, r: t.r });
  }
  return out;
}

/** The hex point-mirrored through the centre of a cols×rows odd-r map. */
export function mirror(h, cols, rows) {
  const { col, row } = toOffset(h);
  return fromOffset(cols - 1 - col, rows - 1 - row);
}

/** Is `h` in the "first half" (the half that symmetric maps copy from)? */
function firstHalf(h, cols, rows) {
  const { col, row } = toOffset(h);
  return row * cols + col < (cols * rows) / 2;
}

/** Copy terrain from the first half onto the mirrored second half. */
export function mirrorMap(map) {
  for (const t of map) {
    if (!firstHalf(t, map.cols, map.rows)) continue;
    const m = map.get(mirror(t, map.cols, map.rows));
    m.terrain = t.terrain;
    m.elevation = t.elevation;
  }
}

/** Terrain for an elevation/moisture pair. */
export function classify(e, m, opts = DEFAULTS) {
  const w = opts.water;
  if (e < w) return "water";
  if (e < w + 0.05) return "shallows";
  if (e < w + 0.08) return m > 0.6 ? "swamp" : "sand";
  if (e > 0.8) return "mountain";
  if (e > 0.68) return m > 0.65 ? "forest" : "hills";
  if (m > 0.72 && e < 0.5) return "swamp";
  if (m > 0.58) return "forest";
  return "plains";
}

/** The largest set of mutually reachable passable tiles (keys). */
export function largestRegion(map) {
  const seen = new Set();
  let best = new Set();
  for (const t of map) {
    const k = key(t);
    if (seen.has(k) || !map.passable(t)) continue;
    const region = floodFill(map, t);
    for (const r of region) seen.add(r);
    if (region.size > best.size) best = region;
  }
  return best;
}

/** Deployment zone: the `size` region hexes nearest `anchor` (spiralling out). */
function zoneAround(map, region, anchor, size, taken) {
  const out = [];
  for (let radius = 0; out.length < size && radius < 12; radius++) {
    for (const h of spiral(anchor, radius)) {
      const k = key(h);
      if (out.length >= size) break;
      if (region.has(k) && !taken.has(k) && map.terrainAt(h).id !== "mountain" && !out.some((o) => key(o) === k)) {
        out.push(h);
        taken.add(k);
      }
    }
  }
  return out;
}

function pickAnchor(map, region, colLo, colHi, rng) {
  const options = [...region].map(fromKey).filter((h) => {
    const { col, row } = toOffset(h);
    return col >= colLo && col <= colHi && row > 1 && row < map.rows - 2 && map.terrainAt(h).cost <= 2;
  });
  if (!options.length) return null;
  // prefer hexes with many passable neighbours (open ground)
  options.sort((a, b) => openness(map, b) - openness(map, a) || toOffset(a).row - toOffset(b).row);
  return rng.pick(options.slice(0, Math.max(1, Math.ceil(options.length / 4))));
}

function openness(map, h) {
  return map.neighbors(h).filter((n) => map.passable(n)).length;
}

/**
 * Generate a battle map.
 * @returns {{map: HexMap, spawns: Array<Array<{q:number,r:number}>>, villages: Array<{q:number,r:number}>,
 *            seed: number, attempts: number}}
 */
export function generate(options = {}) {
  const opts = { ...DEFAULTS, ...options };
  const rng = new RNG(opts.seed);
  for (let attempt = 1; attempt <= 20; attempt++) {
    const result = tryGenerate(opts, rng.fork());
    if (result) return { ...result, seed: opts.seed, attempts: attempt };
  }
  throw new Error(`could not generate a playable map for seed ${opts.seed}`);
}

function tryGenerate(opts, rng) {
  const map = new HexMap(opts.cols, opts.rows);
  const elev = new ValueNoise(Math.floor(rng.next() * 2 ** 31));
  const moist = new ValueNoise(Math.floor(rng.next() * 2 ** 31));
  const ox = rng.next() * 100, oy = rng.next() * 100;
  for (const t of map) {
    const p = toPixel(t, 1);
    const x = p.x * opts.scale + ox, y = p.y * opts.scale + oy;
    const e = elev.fbm(x, y, 4);
    const m = moist.fbm(x + 37.1, y - 11.3, 3);
    t.elevation = e;
    t.terrain = classify(e, m, opts);
  }
  for (const src of riverSources(map, opts.rivers, rng)) {
    const start = map.neighbors(src).sort((x, y) => map.get(x).elevation - map.get(y).elevation)[0];
    if (start && map.passable(start) && map.terrainAt(start).id !== "mountain") carveRiver(map, start);
  }
  if (opts.symmetric) mirrorMap(map);
  const region = largestRegion(map);
  if (region.size < map.size * 0.45) return null;

  const taken = new Set();
  const w = opts.cols;
  const a = pickAnchor(map, region, 0, Math.floor(w * 0.22), rng);
  const b = opts.symmetric && a ? mirror(a, map.cols, map.rows) : pickAnchor(map, region, Math.ceil(w * 0.78), w - 1, rng);
  if (!a || !b || distance(a, b) < w * 0.5) return null;
  const zoneA = zoneAround(map, region, a, opts.spawnSize, taken);
  let zoneB;
  if (opts.symmetric) {
    zoneB = zoneA.map((h) => mirror(h, map.cols, map.rows));
    for (const h of zoneB) taken.add(key(h));
  } else {
    zoneB = zoneAround(map, region, b, opts.spawnSize, taken);
  }
  const spawns = [zoneA, zoneB];
  if (spawns.some((s) => s.length < opts.spawnSize)) return null;

  let villages;
  if (opts.symmetric) {
    const half = placeVillages(map, region, spawns, Math.ceil(opts.villages / 2), rng, taken,
      (h) => firstHalf(h, map.cols, map.rows) && distance(h, mirror(h, map.cols, map.rows)) >= 4);
    villages = [...half, ...half.map((h) => mirror(h, map.cols, map.rows))];
  } else {
    villages = placeVillages(map, region, spawns, opts.villages, rng, taken);
  }
  if (opts.roads) layRoads(map, [a, ...villages.slice().sort((x, y) => toOffset(x).col - toOffset(y).col), b]);
  if (opts.symmetric) mirrorMap(map);
  return { map, spawns, villages };
}

function placeVillages(map, region, spawns, count, rng, taken, allowed = () => true) {
  const spawnHexes = spawns.flat();
  const candidates = rng.shuffle([...region].map(fromKey).filter((h) => {
    const id = map.terrainAt(h).id;
    return (id === "plains" || id === "hills" || id === "sand") && !taken.has(key(h)) && allowed(h);
  }));
  const out = [];
  for (const h of candidates) {
    if (out.length >= count) break;
    if (out.some((v) => distance(v, h) < 4)) continue;
    if (spawnHexes.some((s) => distance(s, h) < 3)) continue;
    map.set(h, "village");
    out.push(h);
  }
  return out;
}

/** Connect consecutive waypoints with roads that prefer existing roads and easy ground. */
function layRoads(map, waypoints) {
  const cost = (_f, to) => {
    const t = map.terrainAt(to);
    if (!t || !Number.isFinite(t.cost)) return Infinity;
    if (t.id === "road" || t.id === "village") return 0.5;
    if (t.id === "shallows") return 4;
    if (t.id === "bridge") return 0.5;
    if (t.id === "river") return 3;
    return 1 + t.cost;
  };
  for (let i = 0; i + 1 < waypoints.length; i++) {
    const res = findPath(map, waypoints[i], waypoints[i + 1], cost);
    if (!res) continue;
    for (const h of res.path) {
      const id = map.terrainAt(h).id;
      if (id === "river") map.set(h, "bridge");
      else if (id !== "village" && id !== "shallows" && id !== "bridge") map.set(h, "road");
    }
  }
}

/** Summary counts of each terrain (handy for tests and the UI legend). */
export function terrainCounts(map) {
  const counts = {};
  for (const t of map) counts[t.terrain] = (counts[t.terrain] ?? 0) + 1;
  return counts;
}

export { terrain, fromOffset };
