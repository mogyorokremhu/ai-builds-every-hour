import { test } from "node:test";
import assert from "node:assert/strict";
import { Game, SIDES, VILLAGE_HEAL } from "../src/game.js";
import { serialize, deserialize, saveToSlot, loadFromSlot, listSlots, deleteSlot, MemoryStorage } from "../src/save.js";
import { key, distance } from "../src/hex.js";
import { maxMp, DEFAULT_ARMY } from "../src/units.js";
import { arena, plainMap } from "./helpers.js";

test("Game.create deploys both armies inside their zones", () => {
  const g = Game.create({ seed: 7 });
  assert.equal(g.units.length, DEFAULT_ARMY.length * 2);
  SIDES.forEach((s, i) => {
    const zone = new Set(g.spawns[i].map(key));
    for (const u of g.unitsOf(s.id)) assert.ok(zone.has(key(u)), `${s.id} unit ${u.id} in zone`);
  });
  assert.equal(new Set(g.units.map(key)).size, g.units.length, "one unit per hex");
  assert.equal(g.side, "red");
  assert.equal(g.turn, 1);
});

test("deploying more units than the zone holds fails", () => {
  const g = new Game({ map: plainMap(), spawns: [[{ q: 3, r: 3 }], []] });
  assert.throws(() => g.deploy("red", ["spearman", "spearman"]));
});

test("move spends MP, can be undone, and is refused out of turn", () => {
  const g = arena([["swordsman", "red", 2, 3], ["spearman", "blue", 7, 3]]);
  const [a, b] = g.units;
  const route = g.move(a, { q: 4, r: 3 });
  assert.equal(route.length, 3);
  assert.deepEqual([a.q, a.r, a.mp], [4, 3, 3]);
  assert.ok(g.canUndo());
  assert.ok(g.undo());
  assert.deepEqual([a.q, a.r, a.mp], [2, 3, 5]);
  assert.equal(g.undo(), false);
  assert.throws(() => g.move(b, { q: 6, r: 3 }), /turn/);
  assert.throws(() => g.move(a, { q: 9, r: 3 }), /reach/);
});

test("entering an enemy zone of control ends the move", () => {
  const g = arena([["cavalry", "red", 2, 3], ["spearman", "blue", 6, 3]]);
  const [cav] = g.units;
  g.move(cav, { q: 5, r: 3 });
  assert.equal(cav.mp, 0);
  assert.ok(g.inZoc(cav));
});

test("several moves per turn while MP lasts; undo walks back step by step", () => {
  const g = arena([["cavalry", "red", 2, 3]]);
  const [c] = g.units;
  g.move(c, { q: 4, r: 3 });
  g.move(c, { q: 6, r: 3 });
  assert.equal(c.mp, 4);
  g.undo();
  assert.deepEqual([c.q, c.mp], [4, 6]);
  g.undo();
  assert.deepEqual([c.q, c.mp], [2, 8]);
});

test("attackPlan moves next to the target when needed and prefers good terrain", () => {
  const map = plainMap(10, 8, { "5,2": "forest" });
  const g = arena([["swordsman", "red", 2, 3], ["spearman", "blue", 5, 3]], { map });
  const [a, t] = g.units;
  const plan = g.attackPlan(a, t);
  assert.equal(distance(plan.from, t), 1);
  assert.equal(key(plan.from), "5,2", "attacks from the forest (25% defence)");
  const res = g.attack(a, t);
  assert.deepEqual([a.q, a.r], [5, 2]);
  assert.ok(a.acted && a.mp === 0);
  assert.ok(res.dealt > 0);
  assert.equal(g.canUndo(), false, "attacking clears the undo history");
  assert.equal(g.attackPlan(a, t), null, "one attack per turn");
});

test("attack refuses impossible targets", () => {
  const g = arena([["swordsman", "red", 0, 1], ["spearman", "blue", 7, 6]]);
  assert.equal(g.attackPlan(g.units[0], g.units[1]), null);
  assert.throws(() => g.attack(g.units[0], g.units[1]));
});

test("routing the last enemy wins the battle", () => {
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "blue", 4, 3]]);
  g.units[1].hp = 1;
  g.attack(g.units[0], g.units[1]);
  assert.equal(g.winner, "red");
  assert.ok(g.log.at(-1).text.includes("wins"));
  assert.throws(() => g.move(g.units[0], { q: 2, r: 3 }), /over/);
  g.endTurn();
  assert.equal(g.side, "red", "no more turns after the end");
});

test("endTurn alternates sides, counts rounds and refreshes units", () => {
  const g = arena([["cavalry", "red", 2, 3], ["cavalry", "blue", 7, 3]]);
  const [r, b] = g.units;
  g.move(r, { q: 4, r: 3 });
  g.endTurn();
  assert.equal(g.side, "blue");
  assert.equal(g.turn, 1);
  assert.equal(b.mp, maxMp(b));
  assert.equal(g.canUndo(), false);
  g.endTurn();
  assert.equal(g.side, "red");
  assert.equal(g.turn, 2);
  assert.equal(r.mp, maxMp(r));
});

test("villages and healers heal at the start of the owner's turn", () => {
  const map = plainMap(10, 8, { "2,3": "village" });
  const g = arena([["swordsman", "red", 2, 3], ["spearman", "red", 5, 3], ["healer", "red", 6, 3],
    ["spearman", "blue", 8, 5]], { map });
  const [inVillage, nextToHealer] = g.units;
  inVillage.hp = 10;
  nextToHealer.hp = 30;
  g.endTurn(); // blue
  g.endTurn(); // red again: upkeep
  assert.equal(inVillage.hp, 10 + VILLAGE_HEAL);
  assert.equal(nextToHealer.hp, 34, "healing never exceeds max HP");
  assert.ok(g.log.some((l) => l.text.includes("heals")));
});

test("ready() lists units that can still act", () => {
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "red", 1, 1], ["spearman", "blue", 4, 3]]);
  assert.equal(g.ready().length, 2);
  g.attack(g.units[0], g.units[2]);
  g.units[1].mp = 0;
  assert.equal(g.ready().length, 0);
});

test("JSON round trip, and a loaded game plays on identically", () => {
  const g = Game.create({ seed: 11 });
  const red = g.unitsOf("red")[0];
  g.move(red, [...g.area(red).values()].find((n) => n.canStop && n.cost > 0).hex);
  g.endTurn();
  const text = serialize(g);
  const h = deserialize(text);
  assert.deepEqual(h.toJSON(), g.toJSON());
  // play the same scripted sequence in both and compare
  for (const game of [g, h]) {
    const sw = game.unitsOf("blue")[0];
    const enemy = game.unitsOf("red")[0];
    enemy.q = sw.q + 1; enemy.r = sw.r; // force contact on the same hex in both games
    if (game.map.passable(enemy) && !game.units.some((u) => u !== enemy && key(u) === key(enemy))) game.attack(sw, enemy);
    game.endTurn();
  }
  assert.deepEqual(h.toJSON(), g.toJSON());
});

test("bad saves give readable errors", () => {
  assert.throws(() => deserialize("{nope"), /invalid JSON/);
  assert.throws(() => deserialize('{"version": 99}'), /version/);
});

test("storage slots: save, list, load, delete", () => {
  const store = new MemoryStorage();
  store.setItem("unrelated", "x");
  const g = Game.create({ seed: 3 });
  saveToSlot(store, "auto", g);
  g.endTurn();
  saveToSlot(store, "manual", g);
  const slots = listSlots(store);
  assert.deepEqual(slots.map((s) => s.slot).sort(), ["auto", "manual"]);
  assert.equal(loadFromSlot(store, "manual").side, "blue");
  assert.equal(loadFromSlot(store, "auto").side, "red");
  deleteSlot(store, "auto");
  assert.equal(loadFromSlot(store, "auto"), null);
  assert.equal(listSlots(store).length, 1);
});
