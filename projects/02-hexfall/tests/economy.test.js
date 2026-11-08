import { test } from "node:test";
import assert from "node:assert/strict";
import { Game, SAVE_VERSION } from "../src/game.js";
import { DEFAULT_RULES, income, ownedVillages, holdTarget, recruitHexes, keepOf, score } from "../src/economy.js";
import { createUnit, UNIT_TYPES } from "../src/units.js";
import { key } from "../src/hex.js";
import { arena, plainMap } from "./helpers.js";

/** A 12×8 field with a keep + 2 castle hexes per side and villages at the given hexes. */
function castleGame({ villages = [{ q: 4, r: 2 }, { q: 4, r: 5 }, { q: 6, r: 3 }], rules = {}, units = [] } = {}) {
  const map = plainMap(12, 8);
  const red = [{ q: 1, r: 3 }, { q: 0, r: 4 }, { q: 1, r: 2 }];
  const blue = [{ q: 9, r: 3 }, { q: 8, r: 4 }, { q: 9, r: 2 }];
  for (const zone of [red, blue]) zone.forEach((h, i) => map.set(h, i === 0 ? "keep" : "castle"));
  for (const v of villages) map.set(v, "village");
  const g = new Game({ map, spawns: [red, blue], villages, rules });
  for (const [type, side, q, r] of units) g.units.push(createUnit(g.nextId++, type, side, { q, r }));
  return g;
}

test("moving onto a village captures it, ends the move and undo gives it back", () => {
  const g = castleGame({ units: [["cavalry", "red", 2, 2], ["spearman", "blue", 10, 6]] });
  const [cav] = g.units;
  g.move(cav, { q: 4, r: 2 });
  assert.equal(g.map.get({ q: 4, r: 2 }).owner, "red");
  assert.equal(cav.mp, 0, "capturing ends the move");
  assert.equal(ownedVillages(g, "red").length, 1);
  assert.match(g.log.at(-1).text, /captures a village/);
  g.undo();
  assert.equal(g.map.get({ q: 4, r: 2 }).owner, null);
  assert.equal(cav.mp, 8);
  // walking onto your own village is just a move
  g.move(cav, { q: 4, r: 2 });
  g.endTurn();
  g.endTurn();
  g.move(cav, { q: 5, r: 2 });
  g.move(cav, { q: 4, r: 2 });
  assert.equal(cav.mp, 6);
});

test("income: base plus villages, collected at the start of each turn", () => {
  const g = castleGame({ units: [["spearman", "red", 4, 2], ["spearman", "blue", 10, 6]] });
  g.map.get({ q: 4, r: 2 }).owner = "red";
  g.map.get({ q: 4, r: 5 }).owner = "red";
  assert.equal(income(g, "red"), DEFAULT_RULES.baseIncome + 2 * DEFAULT_RULES.villageIncome);
  assert.equal(income(g, "blue"), DEFAULT_RULES.baseIncome);
  const start = g.gold[0];
  g.endTurn(); // blue's turn
  assert.equal(g.gold[1], start + DEFAULT_RULES.baseIncome);
  g.endTurn(); // red again
  assert.equal(g.gold[0], start + income(g, "red"));
});

test("recruiting at the keep: costs gold, lands on a castle hex, cannot act this turn", () => {
  const g = castleGame({ rules: { startGold: 40 }, units: [["spearman", "red", 3, 3], ["spearman", "blue", 10, 6]] });
  assert.deepEqual(keepOf(g, 0), { q: 1, r: 3 });
  assert.equal(recruitHexes(g, 0).length, 3);
  const u = g.recruit("archer");
  assert.equal(g.gold[0], 40 - UNIT_TYPES.archer.cost);
  assert.ok(["1,3", "0,4", "1,2"].includes(key(u)));
  assert.equal(u.mp, 0);
  assert.ok(u.acted);
  assert.equal(g.targets(u).length, 0);
  const v = g.recruit("spearman", { q: 0, r: 4 });
  assert.equal(key(v), "0,4");
  assert.match(g.recruitProblem("swordsman"), /needs 17 gold/);
  assert.throws(() => g.recruit("swordsman"), /gold/);
  assert.throws(() => g.recruit("dragon"), /cannot recruit/);
  g.endTurn();
  g.endTurn();
  assert.equal(u.mp, UNIT_TYPES.archer.mp, "recruits are ready next turn");
});

test("an enemy on your keep stops recruiting; full castles too", () => {
  const g = castleGame({ rules: { startGold: 99 }, units: [["spearman", "blue", 1, 3], ["spearman", "red", 6, 6]] });
  assert.equal(recruitHexes(g, 0).length, 0);
  assert.match(g.recruitProblem("spearman"), /enemy holds your keep/);
  const h = castleGame({ rules: { startGold: 99 }, units: [["spearman", "red", 1, 3], ["spearman", "red", 0, 4], ["spearman", "red", 1, 2], ["spearman", "blue", 10, 6]] });
  assert.match(h.recruitProblem("spearman"), /no free castle hex/);
  const plain = arena([["spearman", "red", 1, 1]]);
  assert.match(plain.recruitProblem("spearman"), /no keep/);
});

test("a side with no units but gold and a keep is not routed yet", () => {
  const g = castleGame({ rules: { startGold: 20 }, units: [["mage", "red", 5, 3], ["rogue", "blue", 6, 3]] });
  g.units[1].hp = 1;
  g.attack(g.units[0], g.units[1]);
  assert.equal(g.winner, null, "blue can still recruit");
  g.gold[1] = 0;
  assert.equal(g.checkWinner(), "red");
  assert.equal(g.endReason, "rout");
});

test("holding enough villages for N turns wins", () => {
  const g = castleGame({ rules: { holdTurns: 2 }, units: [["spearman", "red", 3, 3], ["spearman", "blue", 10, 6]] });
  assert.equal(holdTarget(g), 2);
  for (const v of g.villages.slice(0, 2)) g.map.get(v).owner = "red";
  g.endTurn(); // blue
  g.endTurn(); // red holds (1)
  assert.equal(g.hold[0], 1);
  assert.match(g.log.map((l) => l.text).join("\n"), /1 more turn to victory/);
  g.endTurn();
  g.endTurn(); // red holds (2) → wins
  assert.equal(g.winner, "red");
  assert.equal(g.endReason, "hold");
  // losing a village resets the count
  const h = castleGame({ rules: { holdTurns: 3 }, units: [["spearman", "red", 3, 3], ["spearman", "blue", 10, 6]] });
  for (const v of h.villages.slice(0, 2)) h.map.get(v).owner = "red";
  h.endTurn();
  h.endTurn();
  h.map.get(h.villages[0]).owner = "blue";
  h.endTurn();
  h.endTurn();
  assert.equal(h.hold[0], 0);
  assert.equal(holdTarget(castleGame({ villages: [] })), 0);
});

test("the turn limit decides the battle on score (or a draw)", () => {
  const g = castleGame({ rules: { turnLimit: 2 }, units: [["swordsman", "red", 3, 3], ["spearman", "blue", 10, 6]] });
  g.endTurn();
  g.endTurn();
  g.endTurn();
  assert.equal(g.winner, null);
  g.endTurn(); // end of turn 2
  assert.equal(g.endReason, "turns");
  assert.equal(g.winner, "red", "a swordsman outscores a spearman");
  assert.ok(score(g, "red").total > score(g, "blue").total);
  const d = castleGame({ rules: { turnLimit: 1 }, units: [["spearman", "red", 3, 3], ["spearman", "blue", 10, 6]] });
  d.gold = [5, 5 - 2]; // blue will earn its base income at its turn start
  d.endTurn();
  d.endTurn();
  assert.equal(d.winner, "draw");
});

test("economy state survives a save; version 1 saves still load", () => {
  const g = castleGame({ units: [["cavalry", "red", 2, 2], ["spearman", "blue", 10, 6]] });
  g.move(g.units[0], { q: 4, r: 2 });
  g.gold = [7, 9];
  g.hold = [1, 0];
  const data = JSON.parse(JSON.stringify(g.toJSON()));
  assert.equal(data.version, SAVE_VERSION);
  const back = Game.fromJSON(data);
  assert.deepEqual(back.gold, [7, 9]);
  assert.deepEqual(back.hold, [1, 0]);
  assert.equal(back.map.get({ q: 4, r: 2 }).owner, "red");
  const v1 = { ...data, version: 1 };
  delete v1.gold;
  delete v1.hold;
  delete v1.rules;
  const old = Game.fromJSON(v1);
  assert.deepEqual(old.gold, [DEFAULT_RULES.startGold, DEFAULT_RULES.startGold]);
  assert.equal(old.rules.turnLimit, DEFAULT_RULES.turnLimit);
});

test("generated maps get a keep and castle on each deployment zone", () => {
  for (const seed of [1, 7, 12]) {
    const g = Game.create({ seed });
    for (let i = 0; i < 2; i++) {
      assert.equal(g.map.get(g.spawns[i][0]).terrain, "keep");
      for (const h of g.spawns[i].slice(1)) assert.equal(g.map.get(h).terrain, "castle");
    }
    // the castle is full of the starting army; recruiting needs a free hex
    assert.match(g.recruitProblem("spearman"), /no free castle hex/);
  }
});
