import { test } from "node:test";
import assert from "node:assert/strict";
import { normalizeSetup, toGameOptions, setupProblems, armyCost, resolveArmy, MAP_SIZES } from "../src/skirmish.js";
import { Game } from "../src/game.js";

test("normalizeSetup clamps and fills defaults", () => {
  const s = normalizeSetup({ startGold: 9999, turnLimit: -4, size: "huge", seed: "abc", armies: ["bogus"] });
  assert.equal(s.startGold, 500);
  assert.equal(s.turnLimit, 0);
  assert.equal(s.size, "medium");
  assert.equal(s.seed, 1);
  assert.ok(s.armies[0].length > 0 && s.armies[1].length > 0);
});

test("resolveArmy rejects unknown units", () => {
  assert.throws(() => resolveArmy(["dragon"]));
  assert.throws(() => resolveArmy("nope"));
  assert.deepEqual(resolveArmy(["archer"]), ["archer"]);
});

test("setupProblems flags oversize armies; toGameOptions trims them", () => {
  const raw = { size: "small", armies: ["ranged", "standard"] };
  assert.ok(setupProblems(raw).length >= 1);
  const o = toGameOptions(raw);
  assert.ok(o.armies.every((a) => a.length <= MAP_SIZES.small.spawnSize));
  assert.ok(armyCost(o.armies[0]) > 0);
});

test("a configured skirmish creates a playable game with the chosen rules", () => {
  const g = Game.create(toGameOptions({ seed: 5, size: "small", startGold: 77, turnLimit: 12, fog: true, armies: ["cavalry", "infantry"] }));
  assert.equal(g.map.cols, 18);
  assert.equal(g.rules.turnLimit, 12);
  assert.equal(g.rules.fog, true);
  assert.equal(g.gold[0], 77);
  assert.equal(g.unitsOf("red").length, 5);
});
