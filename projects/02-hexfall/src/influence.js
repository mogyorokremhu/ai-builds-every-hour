// Influence maps shared by AI decisions: how much damage each side could bring to every hex
// next turn (threat), the balance between the two (control), and terrain-aware distance
// fields towards goals (enemy units, villages to take).
import { key, distance, spiral, fromOffset } from "./hex.js";
import { MinHeap } from "./pathfind.js";
import { movementArea, destinations, stepCost } from "./movement.js";
import { maxMp, meleeAttack, rangedAttack, unitType } from "./units.js";
import { effectiveRange } from "./combat.js";
import { todMultiplier } from "./timeofday.js";

/**
 * Strongest single strike `u` could make, scaled by the time of day on `turn`
 * (before terrain and armour).
 */
export function strikePower(u, turn) {
  return Math.max(meleeAttack(u), rangedAttack(u)) * todMultiplier(unitType(u).alignment ?? "neutral", turn);
}

/**
 * Hexes each unit of `attackers` could strike next turn: every hex it can reach with full
 * move points, plus everything in melee or ranged reach of those hexes. Each attacker
 * counts once per hex.
 * @param {object} game
 * @param {object[]} attackers
 * @param {number} turn  game turn the strikes would happen on (time of day)
 * @returns {Map<string, {damage:number, count:number, hp:number}>}
 */
export function strikeMap(game, attackers, turn = game.turn ?? 1) {
  const out = new Map();
  for (const u of attackers) {
    if (u.hp <= 0) continue;
    const ghost = { ...u, mp: maxMp(u) };
    const reach = rangedAttack(u) ? Math.max(1, effectiveRange(game, u)) : 1;
    const power = strikePower(u, turn);
    const seen = new Set();
    for (const node of destinations(movementArea(game, ghost))) {
      for (const h of spiral(node.hex, reach)) {
        const k = key(h);
        if (seen.has(k) || !game.map.has(h)) continue;
        seen.add(k);
      }
    }
    for (const k of seen) {
      const cell = out.get(k) ?? { damage: 0, count: 0, hp: 0 };
      cell.damage += power;
      cell.count += 1;
      cell.hp += u.hp;
      out.set(k, cell);
    }
  }
  return out;
}

/**
 * Enemy threat against `side`: what its opponents could bring to each hex on their next turn.
 * `seen` filters the enemies taken into account (fog of war: only the ones `side` can see).
 */
export function threatMap(game, side, seen = () => true) {
  return strikeMap(game, game.units.filter((u) => u.side !== side && seen(u)), (game.turn ?? 1) + (game.active === 0 ? 0 : 1));
}

/**
 * Control of each hex from `side`'s point of view: its own strike power minus the
 * enemy's (positive = we dominate, negative = dangerous ground).
 * @returns {Map<string, number>}
 */
export function controlMap(game, side) {
  const mine = strikeMap(game, game.units.filter((u) => u.side === side));
  const theirs = threatMap(game, side);
  const out = new Map();
  for (const t of game.map) {
    const k = key(t);
    out.set(k, (mine.get(k)?.damage ?? 0) - (theirs.get(k)?.damage ?? 0));
  }
  return out;
}

/**
 * Multi-source Dijkstra: move-point distance from every hex to the nearest of `goals`
 * for `unit`'s movement type (units do not block — this is for long-range planning).
 * @returns {Map<string, number>}
 */
export function distanceField(game, goals, unit = null) {
  const dist = new Map();
  const heap = new MinHeap();
  for (const g of goals) {
    if (!game.map.has(g)) continue;
    dist.set(key(g), 0);
    heap.push(g, 0);
  }
  const cost = (t) => (unit ? stepCost(unit, t) : t?.cost ?? Infinity);
  while (heap.length) {
    const cur = heap.pop();
    const d = dist.get(key(cur));
    for (const n of game.map.neighbors(cur)) {
      // cost of walking from n into cur (goal side), so distances read "from n"
      const step = cost(game.map.terrainAt(cur));
      const enter = Number.isFinite(step) ? step : Infinity;
      if (!Number.isFinite(enter) && d > 0) continue;
      if (!game.map.passable(n)) continue;
      const nd = d + (Number.isFinite(enter) ? enter : 1);
      const nk = key(n);
      if (nd < (dist.get(nk) ?? Infinity)) {
        dist.set(nk, nd);
        heap.push(n, nd);
      }
    }
  }
  return dist;
}

/** Nearest living enemy of `u` by straight hex distance (null if none). */
export function nearestEnemy(game, u) {
  let best = null;
  for (const t of game.units) {
    if (t.side === u.side || t.hp <= 0) continue;
    if (!best || distance(u, t) < distance(u, best)) best = t;
  }
  return best;
}

/** ASCII picture of a numeric hex map (for debugging AI decisions in a terminal). */
export function asciiField(game, values, scale = 1) {
  const rows = [];
  for (let row = 0; row < game.map.rows; row++) {
    let line = row & 1 ? " " : "";
    for (let col = 0; col < game.map.cols; col++) {
      const v = values.get(key(fromOffset(col, row)));
      line += v == null || !Number.isFinite(v) ? "· " : `${Math.min(9, Math.max(0, Math.round(v / scale)))} `;
    }
    rows.push(line.trimEnd());
  }
  return rows.join("\n");
}
