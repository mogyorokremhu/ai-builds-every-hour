import { test } from "node:test";
import assert from "node:assert/strict";
import { frontier, needsScouting, scoutGoals } from "../src/scouting.js";
import { key } from "../src/hex.js";
import { arena, plainMap } from "./helpers.js";

const fogGame = (units) => {
  const g = arena(units, { map: plainMap(16, 8) });
  g.rules.fog = true;
  g.rules.weather = false;
  g.updateVision();
  return g;
};

test("no fog: nothing to scout", () => {
  const g = arena([["spearman", "red", 1, 1], ["spearman", "blue", 8, 4]]);
  assert.deepEqual(frontier(g, "red"), []);
  assert.equal(needsScouting(g, "red"), false);
});

test("frontier hexes are unexplored and touch explored ground", () => {
  const g = fogGame([["spearman", "red", 2, 3], ["spearman", "blue", 14, 3]]);
  const f = frontier(g, "red", 10);
  assert.ok(f.length > 0);
  for (const h of f) assert.ok(!g.explored[0].has(key(h)));
});

test("scouting only while no enemy is visible", () => {
  const far = fogGame([["spearman", "red", 1, 3], ["spearman", "blue", 14, 3]]);
  assert.equal(needsScouting(far, "red"), true);
  assert.ok(scoutGoals(far, "red").length > 0);
  const near = fogGame([["spearman", "red", 4, 3], ["spearman", "blue", 6, 3]]);
  assert.equal(needsScouting(near, "red"), false);
  assert.deepEqual(scoutGoals(near, "red"), []);
});

test("frontier is sorted towards the enemy side", () => {
  const g = fogGame([["spearman", "red", 2, 3], ["spearman", "blue", 14, 3]]);
  g.spawns = [[{ q: 1, r: 3 }], [{ q: 14, r: 3 }]];
  const f = frontier(g, "red", 3);
  assert.ok(f[0].q >= f[f.length - 1].q - 3);
});
