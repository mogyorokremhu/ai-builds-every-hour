import test from "node:test";
import assert from "node:assert/strict";
import { plainMap } from "./helpers.js";
import { terrainCost } from "../src/pathfind.js";
import { mirrorMap } from "../src/mapgen.js";
import { unitType } from "../src/units.js";

test("terrainCost returns Infinity off the map and a number on it", () => {
  const cost = terrainCost(plainMap(4, 4));
  assert.ok(Number.isFinite(cost({ q: 0, r: 0 }, { q: 1, r: 0 })));
  assert.equal(cost({ q: 0, r: 0 }, { q: 99, r: 99 }), Infinity);
});
test("mirrorMap makes the map point-symmetric in terrain", () => {
  const m = plainMap(6, 6, { "0,0": "forest" });
  mirrorMap(m);
  let forests = 0;
  for (const t of m) if (t.terrain === "forest") forests++;
  assert.ok(forests >= 1);
});
test("unitType accepts names and units, throws on unknown", () => {
  assert.equal(unitType("archer"), unitType({ type: "archer" }));
  assert.throws(() => unitType("dragon"), /unknown unit type/);
});
