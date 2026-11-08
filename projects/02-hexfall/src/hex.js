// Hex-grid math on axial coordinates (q, r), pointy-top orientation.
// Reference: Red Blob Games' hexagon guide. Cube coordinates are (q, r, s) with s = -q - r.

/** @typedef {{q: number, r: number}} Hex */

export const DIRECTIONS = Object.freeze([
  { q: 1, r: 0 }, { q: 1, r: -1 }, { q: 0, r: -1 },
  { q: -1, r: 0 }, { q: -1, r: 1 }, { q: 0, r: 1 },
]);

export const SQRT3 = Math.sqrt(3);

/** @returns {Hex} */
export function hex(q, r) {
  return { q, r };
}

export function key(h) {
  return `${h.q},${h.r}`;
}

export function fromKey(k) {
  const [q, r] = k.split(",").map(Number);
  return { q, r };
}

export function equals(a, b) {
  return a.q === b.q && a.r === b.r;
}

export function add(a, b) {
  return { q: a.q + b.q, r: a.r + b.r };
}

export function sub(a, b) {
  return { q: a.q - b.q, r: a.r - b.r };
}

export function scale(a, k) {
  return { q: a.q * k, r: a.r * k };
}

export function neighbor(h, dir) {
  return add(h, DIRECTIONS[((dir % 6) + 6) % 6]);
}

export function neighbors(h) {
  return DIRECTIONS.map((d) => add(h, d));
}

export function distance(a, b) {
  const dq = a.q - b.q;
  const dr = a.r - b.r;
  return (Math.abs(dq) + Math.abs(dr) + Math.abs(dq + dr)) / 2;
}

/** Round fractional axial coordinates to the nearest hex (via cube rounding). */
export function round(fq, fr) {
  const fs = -fq - fr;
  let q = Math.round(fq);
  let r = Math.round(fr);
  const s = Math.round(fs);
  const dq = Math.abs(q - fq);
  const dr = Math.abs(r - fr);
  const ds = Math.abs(s - fs);
  if (dq > dr && dq > ds) q = -r - s;
  else if (dr > ds) r = -q - s;
  return { q: q + 0, r: r + 0 }; // +0 turns -0 into 0
}

/** Hexes on the straight line from a to b (inclusive), sampled at hex centres. */
export function line(a, b) {
  const n = distance(a, b);
  if (n === 0) return [{ ...a }];
  const out = [];
  // nudge to break ties consistently when the line runs along an edge
  const aq = a.q + 1e-6, ar = a.r + 1e-6;
  const bq = b.q + 1e-6, br = b.r + 1e-6;
  for (let i = 0; i <= n; i++) {
    const t = i / n;
    out.push(round(aq + (bq - aq) * t, ar + (br - ar) * t));
  }
  return out;
}

/** All hexes at exactly `radius` steps from `center` (radius 0 -> the centre). */
export function ring(center, radius) {
  if (radius === 0) return [{ ...center }];
  const out = [];
  let h = add(center, scale(DIRECTIONS[4], radius));
  for (let side = 0; side < 6; side++) {
    for (let step = 0; step < radius; step++) {
      out.push(h);
      h = neighbor(h, side);
    }
  }
  return out;
}

/** All hexes within `radius` of `center`, in spiral order (centre first). */
export function spiral(center, radius) {
  const out = [];
  for (let k = 0; k <= radius; k++) out.push(...ring(center, k));
  return out;
}

/** Rotate `h` around `center` by 60° * steps (positive = clockwise on screen). */
export function rotate(h, center, steps = 1) {
  let { q, r } = sub(h, center);
  let s = -q - r;
  const n = ((steps % 6) + 6) % 6;
  for (let i = 0; i < n; i++) [q, r, s] = [-r, -s, -q];
  return add(center, { q: q + 0, r: r + 0 });
}

// ---- pixel conversions (pointy-top) -----------------------------------------
export function toPixel(h, size) {
  return { x: size * SQRT3 * (h.q + h.r / 2), y: size * 1.5 * h.r };
}

export function fromPixel(x, y, size) {
  const q = ((SQRT3 / 3) * x - y / 3) / size;
  const r = ((2 / 3) * y) / size;
  return round(q, r);
}

/** The six corner points of a hex at pixel centre (cx, cy). */
export function corners(cx, cy, size) {
  const out = [];
  for (let i = 0; i < 6; i++) {
    const a = (Math.PI / 180) * (60 * i - 30);
    out.push({ x: cx + size * Math.cos(a), y: cy + size * Math.sin(a) });
  }
  return out;
}

// ---- offset coordinates ("odd-r": odd rows shoved right) ---------------------
export function toOffset(h) {
  return { col: h.q + (h.r - (h.r & 1)) / 2, row: h.r };
}

export function fromOffset(col, row) {
  return { q: col - (row - (row & 1)) / 2, r: row };
}
