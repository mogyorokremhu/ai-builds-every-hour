import { test } from "node:test";
import assert from "node:assert/strict";
import { HexMap } from "../src/map.js";
import { generate, classify, largestRegion, terrainCounts } from "../src/mapgen.js";
import { reachable, pathTo, findPath, floodFill, MinHeap } from "../src/pathfind.js";
import { RNG, seedFrom } from "../src/rng.js";
import { ValueNoise } from "../src/noise.js";
import { key, distance, fromOffset } from "../src/hex.js";

test("rng is deterministic and well-behaved", () => {
  const a = new RNG(42), b = new RNG(42);
  const xs = Array.from({ length: 50 }, () => a.next());
  assert.deepEqual(xs, Array.from({ length: 50 }, () => b.next()));
  for (const x of xs) assert.ok(x >= 0 && x < 1);
  const r = new RNG(1);
  for (let i = 0; i < 200; i++) {
    const n = r.int(3, 5);
    assert.ok(n >= 3 && n <= 5 && Number.isInteger(n));
  }
  assert.equal(r.weighted([["only", 1]]), "only");
  assert.deepEqual(r.shuffle([1, 2, 3, 4]).sort(), [1, 2, 3, 4]);
  assert.throws(() => r.pick([]));
  assert.equal(seedFrom("hexfall"), seedFrom("hexfall"));
  assert.notEqual(seedFrom("a"), seedFrom("b"));
});

test("value noise is smooth and bounded", () => {
  const n = new ValueNoise(3);
  for (let i = 0; i < 100; i++) {
    const v = n.fbm(i * 0.37, i * 0.11);
    assert.ok(v >= 0 && v <= 1);
  }
  assert.ok(Math.abs(n.at(1.5, 2.5) - n.at(1.501, 2.5)) < 0.01);
  assert.equal(n.at(4, 4), new ValueNoise(3).at(4, 4));
});

test("min-heap pops in priority order", () => {
  const h = new MinHeap();
  const r = new RNG(9);
  const vals = Array.from({ length: 100 }, () => r.int(0, 1000));
  vals.forEach((v) => h.push(v, v));
  const out = [];
  while (h.length) out.push(h.pop());
  assert.deepEqual(out, [...vals].sort((x, y) => x - y));
});

function corridorMap() {
  // 6x3 map: plains everywhere, a forest strip, one mountain
  const m = new HexMap(6, 3);
  m.set(fromOffset(2, 1), "forest");
  m.set(fromOffset(3, 1), "mountain");
  return m;
}

test("reachable respects move points, terrain and the free first step", () => {
  const m = corridorMap();
  const start = fromOffset(0, 1);
  const area = reachable(m, start, 2);
  assert.ok(area.has(key(fromOffset(1, 1))));
  assert.ok(!area.has(key(fromOffset(2, 1)))); // 1 plains + forest(2) = 3 > 2
  assert.ok(!area.has(key(fromOffset(3, 1)))); // mountain
  for (const node of area.values()) assert.ok(node.cost <= 2);
  const path = pathTo(area, fromOffset(1, 0));
  assert.deepEqual(path[0], start);
  for (let i = 1; i < path.length; i++) assert.equal(distance(path[i - 1], path[i]), 1);
  // a unit with 1 MP may still step into forest (cost 2) from a standstill
  const slow = new HexMap(3, 1);
  slow.set(fromOffset(1, 0), "swamp");
  assert.ok(reachable(slow, fromOffset(0, 0), 1).has(key(fromOffset(1, 0))));
  assert.ok(!reachable(slow, fromOffset(0, 0), 1, undefined, { minimumStep: false }).has(key(fromOffset(1, 0))));
  assert.equal(pathTo(area, fromOffset(5, 2)), null);
});

test("A* finds optimal paths around obstacles", () => {
  const m = corridorMap();
  const res = findPath(m, fromOffset(0, 1), fromOffset(5, 1));
  assert.ok(res);
  assert.ok(!res.path.some((h) => m.terrainAt(h).id === "mountain"));
  // compare with Dijkstra over the whole map
  const all = reachable(m, fromOffset(0, 1), 99, undefined, { minimumStep: false });
  assert.equal(res.cost, all.get(key(fromOffset(5, 1))).cost);
  const walled = new HexMap(3, 3);
  for (let row = 0; row < 3; row++) walled.set(fromOffset(1, row), "water");
  assert.equal(findPath(walled, fromOffset(0, 1), fromOffset(2, 1)), null);
  assert.equal(floodFill(walled, fromOffset(0, 1)).size, 3);
});

test("classify covers the elevation range", () => {
  assert.equal(classify(0.1, 0.5), "water");
  assert.equal(classify(0.95, 0.5), "mountain");
  assert.equal(classify(0.5, 0.2), "plains");
  assert.equal(classify(0.5, 0.65), "forest");
});

test("map JSON round-trips and draws as ASCII", () => {
  const { map } = generate({ seed: 5 });
  map.get(fromOffset(3, 3)).owner = "red";
  const copy = HexMap.fromJSON(JSON.parse(JSON.stringify(map.toJSON())));
  assert.deepEqual(copy.toJSON(), map.toJSON());
  assert.equal(copy.get(fromOffset(3, 3)).owner, "red");
  const art = map.ascii().split("\n");
  assert.equal(art.length, map.rows);
  assert.ok(art[1].startsWith(" "));
  assert.throws(() => map.set({ q: 999, r: 999 }, "plains"));
  assert.throws(() => map.set(fromOffset(0, 0), "lava"));
});

test("generated maps are deterministic and playable", () => {
  for (let seed = 1; seed <= 25; seed++) {
    const g = generate({ seed });
    const again = generate({ seed });
    assert.deepEqual(g.map.toJSON(), again.map.toJSON(), `seed ${seed} not deterministic`);
    const { map, spawns, villages } = g;
    assert.equal(spawns.length, 2);
    const region = largestRegion(map);
    // both deployment zones lie in one connected region, far apart
    for (const zone of spawns) {
      assert.equal(zone.length, 6);
      for (const h of zone) assert.ok(region.has(key(h)), `seed ${seed}: spawn off the main region`);
    }
    assert.ok(distance(spawns[0][0], spawns[1][0]) >= map.cols * 0.5);
    const path = findPath(map, spawns[0][0], spawns[1][0]);
    assert.ok(path, `seed ${seed}: spawns not connected`);
    // villages are spread out and reachable
    for (const v of villages) {
      assert.equal(map.terrainAt(v).id, "village");
      assert.ok(region.has(key(v)));
    }
    for (let i = 0; i < villages.length; i++)
      for (let j = i + 1; j < villages.length; j++) assert.ok(distance(villages[i], villages[j]) >= 4);
    const counts = terrainCounts(map);
    assert.ok((counts.road ?? 0) > 0, `seed ${seed}: no roads`);
    assert.ok(Object.keys(counts).length >= 4, `seed ${seed}: boring map`);
  }
});

test("different seeds give different maps; options are honoured", () => {
  const a = generate({ seed: 1 }).map.ascii();
  const b = generate({ seed: 2 }).map.ascii();
  assert.notEqual(a, b);
  const small = generate({ seed: 3, cols: 16, rows: 10, villages: 2, roads: false });
  assert.equal(small.map.size, 160);
  assert.ok(small.villages.length <= 2);
  assert.equal(terrainCounts(small.map).road, undefined);
});

test("symmetric maps are point-mirrored, including spawns and villages", async () => {
  const { mirror } = await import("../src/mapgen.js");
  for (let seed = 1; seed <= 12; seed++) {
    const { map, spawns, villages } = generate({ seed, symmetric: true });
    for (const t of map) {
      const m = map.get(mirror(t, map.cols, map.rows));
      assert.equal(m.terrain, t.terrain, `seed ${seed}: asymmetric at ${t.q},${t.r}`);
    }
    assert.deepEqual(spawns[1].map(key), spawns[0].map((h) => key(mirror(h, map.cols, map.rows))));
    const vk = new Set(villages.map(key));
    for (const v of villages) assert.ok(vk.has(key(mirror(v, map.cols, map.rows))));
    assert.ok(findPath(map, spawns[0][0], spawns[1][0]), `seed ${seed}: not connected`);
  }
  const h = fromOffset(2, 3);
  assert.deepEqual(mirror(mirror(h, 24, 16), 24, 16), h);
});

test("rivers flow downhill and roads bridge them", async () => {
  const { carveRiver } = await import("../src/mapgen.js");
  // a slope from left (high) to right (low) ending in the sea
  const m = new HexMap(10, 3);
  for (const t of m) {
    const { col } = m.offsetOf(t);
    t.elevation = 1 - col / 10;
    t.terrain = col === 9 ? "water" : "plains";
  }
  const river = carveRiver(m, fromOffset(0, 1));
  assert.ok(river.length >= 8);
  for (let i = 1; i < river.length; i++) {
    assert.equal(distance(river[i - 1], river[i]), 1);
    assert.ok(m.get(river[i]).elevation <= m.get(river[i - 1]).elevation + 0.08);
  }
  for (const h of river) assert.equal(m.terrainAt(h).id, "river");
  let rivers = 0, bridges = 0;
  for (let seed = 1; seed <= 25; seed++) {
    const c = terrainCounts(generate({ seed }).map);
    rivers += c.river ?? 0;
    bridges += c.bridge ?? 0;
  }
  assert.ok(rivers > 25, `only ${rivers} river hexes in 25 maps`);
  assert.ok(bridges > 0, "roads never bridged a river");
  assert.equal(terrainCounts(generate({ seed: 4, rivers: 0 }).map).river, undefined);
});
