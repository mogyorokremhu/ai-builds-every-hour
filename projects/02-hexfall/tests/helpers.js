// Shared test fixtures: small hand-made battlefields with units placed exactly.
import { HexMap } from "../src/map.js";
import { Game } from "../src/game.js";
import { createUnit } from "../src/units.js";

/** A cols×rows all-plains map, with optional {"q,r": terrain} overrides. */
export function plainMap(cols = 10, rows = 8, terrain = {}) {
  const m = new HexMap(cols, rows);
  for (const [k, id] of Object.entries(terrain)) {
    const [q, r] = k.split(",").map(Number);
    m.set({ q, r }, id);
  }
  return m;
}

/** A game on `map` with `units` = [[type, side, q, r], ...] and no deployment zones. */
export function arena(units, { map = plainMap(), seed = 1 } = {}) {
  const g = new Game({ map, spawns: [[], []], seed });
  for (const [type, side, q, r] of units) g.units.push(createUnit(g.nextId++, type, side, { q, r }));
  return g;
}
