// Seeded pseudo-random numbers (mulberry32) so maps and battles are reproducible.

export class RNG {
  /** @param {number} seed any 32-bit integer */
  constructor(seed = 1) {
    this.state = seed >>> 0;
  }

  /** Uniform float in [0, 1). */
  next() {
    let t = (this.state = (this.state + 0x6d2b79f5) >>> 0);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }

  /** Integer in [lo, hi] inclusive. */
  int(lo, hi) {
    return lo + Math.floor(this.next() * (hi - lo + 1));
  }

  chance(p) {
    return this.next() < p;
  }

  pick(arr) {
    if (!arr.length) throw new Error("pick from empty array");
    return arr[Math.floor(this.next() * arr.length)];
  }

  /** Fisher–Yates shuffle (in place, returns the array). */
  shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(this.next() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  /** Pick from [[item, weight], ...]. */
  weighted(pairs) {
    const total = pairs.reduce((s, [, w]) => s + w, 0);
    let x = this.next() * total;
    for (const [item, w] of pairs) {
      x -= w;
      if (x < 0) return item;
    }
    return pairs[pairs.length - 1][0];
  }

  /** An independent generator derived from this one (for sub-systems). */
  fork() {
    return new RNG(Math.floor(this.next() * 4294967296));
  }
}

/** Hash a string to a 32-bit seed (FNV-1a). */
export function seedFrom(text) {
  let h = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return h >>> 0;
}
