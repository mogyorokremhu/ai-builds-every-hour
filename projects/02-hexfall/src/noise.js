// 2D value noise with fractal octaves — smooth, seeded, dependency-free terrain fields.
import { RNG } from "./rng.js";

export class ValueNoise {
  constructor(seed = 1, size = 256) {
    const rng = new RNG(seed);
    this.size = size;
    this.values = Float64Array.from({ length: size }, () => rng.next());
    this.perm = rng.shuffle([...Array(size).keys()]);
  }

  lattice(ix, iy) {
    const s = this.size;
    const p = this.perm[(((ix % s) + s) % s)];
    return this.values[this.perm[(((p + iy) % s) + s) % s]];
  }

  /** Smooth noise in [0, 1] at (x, y). */
  at(x, y) {
    const ix = Math.floor(x), iy = Math.floor(y);
    const fx = x - ix, fy = y - iy;
    const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
    const a = this.lattice(ix, iy), b = this.lattice(ix + 1, iy);
    const c = this.lattice(ix, iy + 1), d = this.lattice(ix + 1, iy + 1);
    const top = a + (b - a) * sx;
    const bottom = c + (d - c) * sx;
    return top + (bottom - top) * sy;
  }

  /** Fractal Brownian motion: `octaves` layers, each double frequency / half amplitude. */
  fbm(x, y, octaves = 4, lacunarity = 2, gain = 0.5) {
    let amp = 1, freq = 1, sum = 0, norm = 0;
    for (let i = 0; i < octaves; i++) {
      sum += amp * this.at(x * freq, y * freq);
      norm += amp;
      amp *= gain;
      freq *= lacunarity;
    }
    return sum / norm;
  }
}
