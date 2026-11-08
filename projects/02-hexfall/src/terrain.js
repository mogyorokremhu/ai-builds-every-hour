// Terrain types: movement cost, defence bonus, sight blocking and colours.

/**
 * @typedef {object} Terrain
 * @property {string} id
 * @property {string} name
 * @property {number} cost      movement points to enter (Infinity = impassable)
 * @property {number} defense   % damage reduction for a unit standing here
 * @property {boolean} blocksSight
 * @property {number} height    0 = sea level; high ground gives archers range
 * @property {string} color     base fill colour
 */

/** @type {Record<string, Terrain>} */
export const TERRAIN = Object.freeze({
  water: { id: "water", name: "Water", cost: Infinity, defense: 0, blocksSight: false, height: 0, color: "#2f5d8a" },
  shallows: { id: "shallows", name: "Shallows", cost: 3, defense: -10, blocksSight: false, height: 0, color: "#4f86b0" },
  sand: { id: "sand", name: "Sand", cost: 2, defense: 0, blocksSight: false, height: 1, color: "#d8c78a" },
  plains: { id: "plains", name: "Plains", cost: 1, defense: 0, blocksSight: false, height: 1, color: "#8fb35a" },
  forest: { id: "forest", name: "Forest", cost: 2, defense: 25, blocksSight: true, height: 1, color: "#3f7a3a" },
  swamp: { id: "swamp", name: "Swamp", cost: 3, defense: -10, blocksSight: false, height: 1, color: "#5f7a52" },
  hills: { id: "hills", name: "Hills", cost: 2, defense: 20, blocksSight: false, height: 2, color: "#a99662" },
  mountain: { id: "mountain", name: "Mountain", cost: Infinity, defense: 0, blocksSight: true, height: 3, color: "#8a8580" },
  river: { id: "river", name: "River", cost: 3, defense: -10, blocksSight: false, height: 0, color: "#3d78b0" },
  bridge: { id: "bridge", name: "Bridge", cost: 1, defense: 0, blocksSight: false, height: 1, color: "#9b7b52" },
  village: { id: "village", name: "Village", cost: 1, defense: 30, blocksSight: true, height: 1, color: "#c98a4b" },
  road: { id: "road", name: "Road", cost: 0.5, defense: 0, blocksSight: false, height: 1, color: "#b9a37a" },
});

export function terrain(id) {
  const t = TERRAIN[id];
  if (!t) throw new Error(`unknown terrain ${id}`);
  return t;
}

export function passable(id) {
  return Number.isFinite(terrain(id).cost);
}
