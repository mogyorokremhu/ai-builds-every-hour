import { test } from "node:test";
import assert from "node:assert/strict";
import { generate, terrainCounts, placeRuins, placeFords, largestRegion, mirror } from "../src/mapgen.js";
import { HexMap, CODES } from "../src/map.js";
import { RNG } from "../src/rng.js";
import { key, distance } from "../src/hex.js";
import { terrain } from "../src/terrain.js";
import { plainMap } from "./helpers.js";

test("generated maps carry ruins away from camps and villages", () => {
  let total = 0;
  for (let seed = 1; seed <= 15; seed++) {
    const g = generate({ seed });
    const ruins = [...g.map].filter((t) => t.terrain === "ruins");
    total += ruins.length;
    for (const r of ruins) {
      for (const s of g.spawns.flat()) assert.ok(distance(r, s) >= 4, `seed ${seed}`);
      for (const v of g.villages) assert.ok(distance(r, v) >= 3);
    }
  }
  assert.ok(total >= 20, `ruins placed: ${total}`);
});

test("fords sit on rivers between dry banks, never next to bridges", () => {
  let fords = 0;
  for (let seed = 1; seed <= 20; seed++) {
    const { map } = generate({ seed });
    for (const t of map) {
      if (t.terrain !== "ford") continue;
      fords += 1;
      const ns = map.neighbors(t).map((n) => map.terrainAt(n).id);
      assert.ok(!ns.includes("bridge"), `seed ${seed} ford next to a bridge`);
    }
  }
  assert.ok(fords >= 10, `fords: ${fords}`);
  assert.ok(terrain("ford").cost < terrain("river").cost);
});

test("symmetric maps mirror ruins and fords too", () => {
  for (const seed of [3, 8, 13]) {
    const { map } = generate({ seed, symmetric: true });
    for (const t of map) {
      if (t.terrain !== "ruins" && t.terrain !== "ford") continue;
      assert.equal(map.get(mirror(t, map.cols, map.rows)).terrain, t.terrain, `seed ${seed} ${key(t)}`);
    }
  }
});

test("placeRuins and placeFords respect their counts", () => {
  const map = plainMap(16, 10);
  const region = largestRegion(map);
  const out = placeRuins(map, region, [[{ q: 0, r: 0 }]], [], 3, new RNG(5));
  assert.equal(out.length, 3);
  for (let i = 0; i < out.length; i++) for (let j = i + 1; j < out.length; j++) assert.ok(distance(out[i], out[j]) >= 5);
  assert.deepEqual(placeRuins(map, region, [], [], 0, new RNG(1)), []);
  const river = plainMap(10, 3);
  for (let q = 0; q < 10; q++) if (river.has({ q: q - 0, r: 1 })) river.set({ q, r: 1 }, "river");
  const f = placeFords(river, 2, new RNG(2));
  assert.ok(f.length >= 1 && f.length <= 2);
  for (const h of f) assert.equal(river.get(h).terrain, "ford");
});

test("ruins, fords and fires survive the map save format", () => {
  const map = plainMap(6, 4, { "1,1": "ruins", "2,1": "ford" });
  map.get({ q: 3, r: 2 }).fire = 2;
  const back = HexMap.fromJSON(JSON.parse(JSON.stringify(map.toJSON())));
  assert.equal(back.get({ q: 1, r: 1 }).terrain, "ruins");
  assert.equal(back.get({ q: 2, r: 1 }).terrain, "ford");
  assert.equal(back.get({ q: 3, r: 2 }).fire, 2);
  assert.equal(back.burning().length, 1);
  assert.equal(CODES.ruins, "u");
  assert.ok(terrainCounts(back).ruins === 1);
});
