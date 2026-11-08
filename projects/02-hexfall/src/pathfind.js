// Movement: Dijkstra "reachable area" for a unit's move points, and A* for long paths.
import { key, distance } from "./hex.js";

/**
 * Cost to step onto `to`. Returns Infinity for impassable or blocked hexes.
 * @callback CostFn
 * @param {{q:number,r:number}} from
 * @param {{q:number,r:number}} to
 * @returns {number}
 */

/** Binary min-heap keyed by priority. */
export class MinHeap {
  constructor() {
    this.items = [];
  }
  get length() {
    return this.items.length;
  }
  push(value, priority) {
    const a = this.items;
    a.push({ value, priority });
    let i = a.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (a[p].priority <= a[i].priority) break;
      [a[p], a[i]] = [a[i], a[p]];
      i = p;
    }
  }
  pop() {
    const a = this.items;
    const top = a[0];
    const last = a.pop();
    if (a.length) {
      a[0] = last;
      let i = 0;
      for (;;) {
        const l = 2 * i + 1, r = l + 1;
        let m = i;
        if (l < a.length && a[l].priority < a[m].priority) m = l;
        if (r < a.length && a[r].priority < a[m].priority) m = r;
        if (m === i) break;
        [a[m], a[i]] = [a[i], a[m]];
        i = m;
      }
    }
    return top?.value;
  }
}

/** The default cost function: terrain movement cost, impassable off-map. */
export function terrainCost(map) {
  return (_from, to) => {
    const t = map.terrainAt(to);
    return t ? t.cost : Infinity;
  };
}

/**
 * Every hex reachable from `start` with at most `budget` move points.
 * A unit may always take one step into a passable neighbour if it has its full budget
 * (so slow terrain never fully pins a fresh unit) — set `minimumStep` to false to disable.
 * @returns {Map<string, {hex: {q:number,r:number}, cost: number, prev: string|null}>}
 */
export function reachable(map, start, budget, costFn = terrainCost(map), { minimumStep = true } = {}) {
  const best = new Map([[key(start), { hex: start, cost: 0, prev: null }]]);
  const heap = new MinHeap();
  heap.push(start, 0);
  while (heap.length) {
    const cur = heap.pop();
    const ck = key(cur);
    const base = best.get(ck).cost;
    for (const n of map.neighbors(cur)) {
      const step = costFn(cur, n);
      if (!Number.isFinite(step)) continue;
      let total = base + step;
      if (total > budget) {
        if (!(minimumStep && base === 0 && budget > 0)) continue;
        total = budget; // the one free full-budget step
      }
      const nk = key(n);
      const old = best.get(nk);
      if (!old || total < old.cost) {
        best.set(nk, { hex: n, cost: total, prev: ck });
        if (total < budget) heap.push(n, total);
      }
    }
  }
  return best;
}

/** Walk the `prev` links of a `reachable` result back to the start. */
export function pathTo(area, target) {
  const tk = key(target);
  if (!area.has(tk)) return null;
  const out = [];
  let k = tk;
  while (k !== null) {
    const node = area.get(k);
    out.push(node.hex);
    k = node.prev;
  }
  return out.reverse();
}

/**
 * A* from `start` to `goal`. Returns {path, cost} or null when unreachable.
 * The heuristic is hex distance × the cheapest step cost (`minStep`, default 0.5 for roads).
 */
export function findPath(map, start, goal, costFn = terrainCost(map), { minStep = 0.5, maxNodes = 20000 } = {}) {
  const gk = key(goal);
  const g = new Map([[key(start), 0]]);
  const prev = new Map([[key(start), null]]);
  const heap = new MinHeap();
  heap.push(start, distance(start, goal) * minStep);
  let expanded = 0;
  const closed = new Set();
  while (heap.length) {
    const cur = heap.pop();
    const ck = key(cur);
    if (closed.has(ck)) continue;
    closed.add(ck);
    if (ck === gk) {
      const path = [];
      let k = ck;
      let h = cur;
      while (k !== null) {
        path.push(h);
        k = prev.get(k);
        if (k !== null) {
          const [q, r] = k.split(",").map(Number);
          h = { q, r };
        }
      }
      return { path: path.reverse(), cost: g.get(gk) };
    }
    if (++expanded > maxNodes) break;
    for (const n of map.neighbors(cur)) {
      const step = costFn(cur, n);
      if (!Number.isFinite(step)) continue;
      const nk = key(n);
      const cost = g.get(ck) + step;
      if (!g.has(nk) || cost < g.get(nk)) {
        g.set(nk, cost);
        prev.set(nk, ck);
        heap.push(n, cost + distance(n, goal) * minStep);
      }
    }
  }
  return null;
}

/** Hexes connected to `start` through passable terrain (flood fill). */
export function floodFill(map, start, passableFn = (h) => map.passable(h)) {
  const seen = new Set([key(start)]);
  const stack = [start];
  while (stack.length) {
    const cur = stack.pop();
    for (const n of map.neighbors(cur)) {
      const nk = key(n);
      if (!seen.has(nk) && passableFn(n)) {
        seen.add(nk);
        stack.push(n);
      }
    }
  }
  return seen;
}
