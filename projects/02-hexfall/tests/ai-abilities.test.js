import { test } from "node:test";
import assert from "node:assert/strict";
import { AIPlayer } from "../src/ai.js";
import { runMatch } from "../src/selfplay.js";
import { abilityPreview } from "../src/abilities.js";
import { key } from "../src/hex.js";
import { arena, plainMap } from "./helpers.js";

test("the AI heals a badly hurt neighbour instead of idling", () => {
  const g = arena([["healer", "red", 3, 3], ["swordsman", "red", 4, 3], ["spearman", "blue", 9, 6]]);
  g.units[1].hp = 8;
  g.units[1].acted = true; // the swordsman is done; only the healer can act
  g.units[1].mp = 0;
  const ai = new AIPlayer("red", { difficulty: "hard" });
  const a = ai.nextAction(g);
  assert.equal(a.type, "ability");
  assert.equal(a.ability, "heal");
  assert.equal(key(a.target), key(g.units[1]));
  ai.play(g, a);
  assert.ok(g.units[1].hp > 8);
});

test("the AI fires a volley into a cluster rather than a single shot", () => {
  const g = arena([["archer", "red", 2, 3], ["spearman", "blue", 5, 3], ["spearman", "blue", 6, 3], ["spearman", "blue", 5, 4], ["spearman", "blue", 6, 2]]);
  const ai = new AIPlayer("red", { difficulty: "hard" });
  const a = ai.nextAction(g);
  assert.equal(a.type, "ability", JSON.stringify(a));
  assert.equal(a.ability, "volley");
});

test("the AI scores friendly fire as a loss", () => {
  const g = arena([["mage", "red", 3, 3], ["swordsman", "red", 5, 3], ["spearman", "blue", 6, 3]]);
  const ai = new AIPlayer("red", { difficulty: "hard" });
  const ctx = ai.context(g);
  const onFriend = abilityPreview(g, g.units[0], "fireball", { q: 5, r: 3 });
  assert.equal(onFriend.hits.length, 2, "the swordsman takes the full blast, the spearman the edge");
  assert.equal(ai.abilityScore(g, g.units[0], g.units[0], onFriend, ctx), 0, "never worth burning your own swordsman");
});

test("endgame: a trailing AI values villages more, a leading one plays safer", () => {
  const map = plainMap(12, 8, { "6,3": "village" });
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "blue", 10, 6]], { map });
  g.villages = [{ q: 6, r: 3 }];
  const ai = new AIPlayer("red", { difficulty: "hard" });
  g.rules.turnLimit = 30;
  g.turn = 5;
  const early = ai.context(g);
  g.turn = 29;
  const late = ai.context(g);
  assert.equal(early.endgame, false);
  assert.equal(late.endgame, true);
  g.gold = [0, 200]; // red is far behind on points
  const behind = ai.context(g);
  assert.ok(behind.lead < 0);
  const v = { q: 6, r: 3 };
  assert.ok(ai.positionScore(g, g.units[0], v, behind) > ai.positionScore(g, g.units[0], v, early));
});

test("guards: an owned village with raiders nearby is worth standing on", () => {
  const map = plainMap(12, 8, { "5,3": "village" });
  map.get({ q: 5, r: 3 }).owner = "red";
  const g = arena([["spearman", "red", 4, 3], ["cavalry", "blue", 9, 3]], { map });
  g.villages = [{ q: 5, r: 3 }];
  const ai = new AIPlayer("red", { difficulty: "hard" });
  const ctx = ai.context(g);
  assert.ok(ctx.guard.has("5,3"));
  g.units[1].q = 11; g.units[1].r = 7; // raider far away
  assert.equal(ai.context(g).guard.size, 0);
});

test("contesting holds: enemy villages are worth more while the enemy is holding", () => {
  const map = plainMap(12, 8, { "6,3": "village" });
  map.get({ q: 6, r: 3 }).owner = "blue";
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "blue", 10, 6]], { map });
  g.villages = [{ q: 6, r: 3 }];
  const ai = new AIPlayer("red", { difficulty: "hard" });
  const calm = ai.positionScore(g, g.units[0], { q: 6, r: 3 }, ai.context(g));
  g.hold = [0, 2];
  const ctx = ai.context(g);
  assert.ok(ctx.foeHolding);
  assert.ok(ai.positionScore(g, g.units[0], { q: 6, r: 3 }, ctx) > calm);
});

test("self-play battles use abilities and report them", () => {
  const r = runMatch({ seed: 2, rules: { turnLimit: 16 } });
  const used = Object.values(r.abilities).reduce((s, n) => s + n, 0);
  assert.ok(used > 5, JSON.stringify(r.abilities));
  assert.ok(r.winner);
});
