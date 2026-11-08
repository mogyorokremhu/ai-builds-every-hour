// Unit movement on the battle map: move costs, unit blocking and zones of control.
import { key, neighbors } from "./hex.js";
import { MinHeap } from "./pathfind.js";
import { hasTrait, maxMp } from "./units.js";

/** Terrains that cost mounted units one extra move point. */
export const ROUGH_FOR_MOUNTS = new Set(["forest", "swamp"]);

/** Move points `unit` pays to enter a hex of terrain `t` (Infinity = cannot enter). */
export function stepCost(unit, t) {
  if (!t || !Number.isFinite(t.cost)) return Infinity;
  return t.cost + (hasTrait(unit, "mounted") && ROUGH_FOR_MOUNTS.has(t.id) ? 1 : 0);
}

/** Set of hex keys adjacent to living enemies of `side` (their zone of control). */
export function enemyZoc(game, side) {
  const zoc = new Set();
  for (const u of game.units) {
    if (u.side === side || u.hp <= 0) continue;
    for (const n of neighbors(u)) zoc.add(key(n));
  }
  return zoc;
}

/**
 * Where can `unit` go this turn?
 * - enemy units block their hex; friendly units can be passed through but not stopped on;
 * - entering a hex in an enemy zone of control (adjacent to an enemy) ends the move there;
 * - a unit that has not moved yet may always take one step onto passable ground, even if
 *   the step costs more than its move points.
 * @param {object} game  anything with `map` and `units`
 * @returns {Map<string, {hex:{q:number,r:number}, cost:number, prev:string|null, zoc:boolean, canStop:boolean}>}
 */
export function movementArea(game, unit) {
  const { map } = game;
  const budget = unit.mp;
  const occupant = new Map(game.units.filter((u) => u.hp > 0).map((u) => [key(u), u]));
  const zoc = enemyZoc(game, unit.side);
  const start = { q: unit.q, r: unit.r };
  const best = new Map([[key(start), { hex: start, cost: 0, prev: null, zoc: false, canStop: true }]]);
  if (budget <= 0) return best;
  const fresh = unit.mp >= maxMp(unit);
  const heap = new MinHeap();
  heap.push(start, 0);
  while (heap.length) {
    const cur = heap.pop();
    const ck = key(cur);
    const node = best.get(ck);
    if (node.zoc && ck !== key(start)) continue; // stopped by a zone of control
    for (const n of map.neighbors(cur)) {
      const nk = key(n);
      const other = occupant.get(nk);
      if (other && other.side !== unit.side) continue;
      const step = stepCost(unit, map.terrainAt(n));
      if (!Number.isFinite(step)) continue;
      let total = node.cost + step;
      if (total > budget) {
        if (!(fresh && node.cost === 0)) continue;
        total = budget; // the one free full-budget step
      }
      const old = best.get(nk);
      if (!old || total < old.cost) {
        best.set(nk, { hex: n, cost: total, prev: ck, zoc: zoc.has(nk), canStop: !other });
        if (total < budget) heap.push(n, total);
      }
    }
  }
  return best;
}

/** Hexes `unit` may end its move on (excludes friendly-occupied hexes; includes its own). */
export function destinations(area) {
  return [...area.values()].filter((n) => n.canStop);
}

/** The route (list of hexes from the unit's hex) to `target` inside `area`, or null. */
export function routeTo(area, target) {
  let k = key(target);
  if (!area.has(k) || !area.get(k).canStop) return null;
  const out = [];
  while (k !== null) {
    const node = area.get(k);
    out.push(node.hex);
    k = node.prev;
  }
  return out.reverse();
}
