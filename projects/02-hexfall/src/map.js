// The battle map: a set of hex tiles with terrain, plus helpers for bounds and lookup.
import { key, neighbors, fromOffset, toOffset } from "./hex.js";
import { terrain, passable } from "./terrain.js";

/**
 * @typedef {object} Tile
 * @property {number} q
 * @property {number} r
 * @property {string} terrain   id from TERRAIN
 * @property {number} elevation 0..1 noise value used by the generator
 * @property {string|null} owner  village owner (side id) or null
 */

export class HexMap {
  /** @param {number} cols @param {number} rows rectangular "odd-r" layout */
  constructor(cols, rows) {
    this.cols = cols;
    this.rows = rows;
    /** @type {Map<string, Tile>} */
    this.tiles = new Map();
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const { q, r } = fromOffset(col, row);
        this.tiles.set(key({ q, r }), { q, r, terrain: "plains", elevation: 0.5, owner: null });
      }
    }
  }

  get size() {
    return this.tiles.size;
  }

  has(h) {
    return this.tiles.has(key(h));
  }

  get(h) {
    return this.tiles.get(key(h)) ?? null;
  }

  set(h, terrainId) {
    const t = this.get(h);
    if (!t) throw new Error(`hex ${key(h)} is off the map`);
    terrain(terrainId); // validate
    t.terrain = terrainId;
  }

  terrainAt(h) {
    const t = this.get(h);
    return t ? terrain(t.terrain) : null;
  }

  passable(h) {
    const t = this.get(h);
    return !!t && passable(t.terrain);
  }

  /** Neighbouring tiles that exist on the map. */
  neighbors(h) {
    return neighbors(h).filter((n) => this.has(n));
  }

  *[Symbol.iterator]() {
    yield* this.tiles.values();
  }

  /** Tiles whose terrain is in `ids`. */
  ofTerrain(...ids) {
    return [...this].filter((t) => ids.includes(t.terrain));
  }

  offsetOf(h) {
    return toOffset(h);
  }

  /** Plain-data copy (for saves and tests). */
  toJSON() {
    const rows = [];
    for (let row = 0; row < this.rows; row++) {
      let line = "";
      for (let col = 0; col < this.cols; col++) {
        line += CODES[this.get(fromOffset(col, row)).terrain];
      }
      rows.push(line);
    }
    const owners = [...this].filter((t) => t.owner).map((t) => [t.q, t.r, t.owner]);
    // elevation (used for shading) in tile order, as whole percent
    const elevation = [...this].map((t) => Math.round(t.elevation * 100));
    return { cols: this.cols, rows: this.rows, terrain: rows, owners, elevation };
  }

  static fromJSON(data) {
    const m = new HexMap(data.cols, data.rows);
    data.terrain.forEach((line, row) => {
      [...line].forEach((ch, col) => {
        const id = DECODE[ch];
        if (!id) throw new Error(`bad terrain code ${ch}`);
        m.set(fromOffset(col, row), id);
      });
    });
    for (const [q, r, owner] of data.owners ?? []) m.get({ q, r }).owner = owner;
    if (data.elevation) [...m].forEach((t, i) => { t.elevation = (data.elevation[i] ?? 50) / 100; });
    return m;
  }

  /** ASCII picture (one char per tile, odd rows indented) for tests and debugging. */
  ascii() {
    const out = [];
    for (let row = 0; row < this.rows; row++) {
      let line = row & 1 ? " " : "";
      for (let col = 0; col < this.cols; col++) {
        line += CODES[this.get(fromOffset(col, row)).terrain] + " ";
      }
      out.push(line.trimEnd());
    }
    return out.join("\n");
  }
}

export const CODES = Object.freeze({
  water: "~", shallows: "-", sand: ":", plains: ".", forest: "f", swamp: "%",
  hills: "n", mountain: "^", village: "V", road: "=", river: "w", bridge: "#",
});
const DECODE = Object.fromEntries(Object.entries(CODES).map(([k, v]) => [v, k]));
