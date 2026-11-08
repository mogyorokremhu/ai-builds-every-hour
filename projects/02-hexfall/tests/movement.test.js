import { test } from "node:test";
import assert from "node:assert/strict";
import { movementArea, destinations, routeTo, enemyZoc, stepCost } from "../src/movement.js";
import { key, distance, neighbors } from "../src/hex.js";
import { terrain } from "../src/terrain.js";
import { createUnit } from "../src/units.js";
import { arena, plainMap } from "./helpers.js";

test("open plains: a 5-MP unit reaches every hex within 5", () => {
  const g = arena([["swordsman", "red", 3, 3]]);
  const area = movementArea(g, g.units[0]);
  for (const t of g.map) {
    const d = distance(t, g.units[0]);
    assert.equal(area.has(key(t)), d <= 5, `${key(t)} at distance ${d}`);
  }
});

test("enemies block their hex and their zone of control stops movement", () => {
  const g = arena([["swordsman", "red", 2, 3], ["spearman", "blue", 5, 3]]);
  const area = movementArea(g, g.units[0]);
  assert.ok(!area.has("5,3"), "cannot enter the enemy hex");
  const zoc = enemyZoc(g, "red");
  assert.equal(zoc.size, 6);
  for (const n of neighbors({ q: 5, r: 3 })) {
    const node = area.get(key(n));
    if (node) assert.ok(node.zoc);
  }
  // the hex behind the enemy is only reachable around the zone of control
  const behind = area.get("6,3");
  assert.ok(!behind || behind.cost > 4, "no straight walk through the ZOC");
  // nothing beyond a ZOC hex is reached *through* it
  for (const node of area.values()) {
    if (node.prev && area.get(node.prev).zoc && node.prev !== key(g.units[0])) assert.fail(`${key(node.hex)} reached through ZOC`);
  }
});

test("friendly units can be passed but not stopped on", () => {
  const g = arena([["swordsman", "red", 2, 3], ["spearman", "red", 3, 3]]);
  const area = movementArea(g, g.units[0]);
  assert.ok(area.has("3,3") && !area.get("3,3").canStop);
  assert.ok(area.has("4,3") && area.get("4,3").cost === 2);
  assert.equal(routeTo(area, { q: 3, r: 3 }), null);
  assert.deepEqual(routeTo(area, { q: 4, r: 3 }).map(key), ["2,3", "3,3", "4,3"]);
  assert.ok(!destinations(area).some((n) => key(n.hex) === "3,3"));
});

test("mounted units pay +1 in forest and swamp", () => {
  const cav = createUnit(1, "cavalry", "red", { q: 0, r: 0 });
  const inf = createUnit(2, "spearman", "red", { q: 0, r: 0 });
  assert.equal(stepCost(cav, terrain("forest")), 3);
  assert.equal(stepCost(inf, terrain("forest")), 2);
  assert.equal(stepCost(cav, terrain("hills")), 2);
  assert.equal(stepCost(cav, terrain("water")), Infinity);
});

test("a fresh unit may always take one step; a moved one may not", () => {
  const map = plainMap(10, 8, { "4,3": "swamp" });
  const g = arena([["spearman", "red", 3, 3]], { map });
  const u = g.units[0];
  u.mp = 2; // pretend it is a 2 MP unit at full points
  u.bonus.mp = -3;
  assert.ok(movementArea(g, u).has("4,3"), "full MP: the free first step");
  u.mp = 1.5;
  assert.ok(!movementArea(g, u).has("4,3"), "already moved: no free step");
});

test("a unit with no move points stays put", () => {
  const g = arena([["spearman", "red", 3, 3]]);
  g.units[0].mp = 0;
  assert.equal(movementArea(g, g.units[0]).size, 1);
});
