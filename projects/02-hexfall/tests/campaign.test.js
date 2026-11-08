import { test } from "node:test";
import assert from "node:assert/strict";
import { SCENARIOS, scenarioOptions, carryOver, restoreVeterans, newProgress, advance, campaignDone } from "../src/campaign.js";
import { Game } from "../src/game.js";

test("there are five scenarios and each builds a game", () => {
  assert.equal(SCENARIOS.length, 5);
  for (let i = 0; i < 5; i++) {
    const g = Game.create(scenarioOptions(i));
    assert.ok(g.unitsOf("blue").length >= 3);
  }
  assert.throws(() => scenarioOptions(9));
});

test("veterans carry over with level, perks and full health", () => {
  const g = Game.create(scenarioOptions(0));
  const u = g.unitsOf("red")[0];
  Object.assign(u, { level: 2, xp: 30, kills: 3, perks: ["x"], hp: 1 });
  u.bonus.attack = 2;
  const roster = carryOver(g);
  const g2 = Game.create({ ...scenarioOptions(1), armies: [[], ["archer"]] });
  const placed = restoreVeterans(g2, "red", roster);
  assert.equal(placed.length, roster.length);
  assert.equal(placed[0].level, 2);
  assert.equal(placed[0].bonus.attack, 2);
  assert.deepEqual(placed[0].perks, ["x"]);
  assert.ok(placed[0].hp > 1);
});

test("dead units are not carried over; progress advances only on a win", () => {
  const g = Game.create(scenarioOptions(0));
  g.unitsOf("red")[0].hp = 0;
  assert.equal(carryOver(g).length, g.unitsOf("red").length - 1);
  let p = newProgress();
  g.winner = "blue";
  p = advance(p, g);
  assert.equal(p.index, 0); assert.equal(p.lost, 1);
  g.winner = "red";
  p = advance(p, g);
  assert.equal(p.index, 1); assert.equal(p.won, 1);
  for (let i = 0; i < 6; i++) p = advance(p, g);
  assert.ok(campaignDone(p));
});
