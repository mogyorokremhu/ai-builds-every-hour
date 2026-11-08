import { test } from "node:test";
import assert from "node:assert/strict";
import { sightRadius, viewFrom, visibleHexes, hiddenEnemies, remember, DEFAULT_SIGHT } from "../src/fog.js";
import { Game } from "../src/game.js";
import { AIPlayer } from "../src/ai.js";
import { key } from "../src/hex.js";
import { arena, plainMap } from "./helpers.js";

const fogArena = (units, map) => {
  const g = arena(units, { map });
  g.rules.fog = true;
  g.rules.weather = false;
  g.updateVision();
  return g;
};

test("sight radius: type default, hills +1", () => {
  const g = arena([["spearman", "red", 2, 2], ["cavalry", "red", 4, 4]], { map: plainMap(10, 8, { "4,4": "hills" }) });
  g.rules.weather = false;
  assert.equal(sightRadius(g, g.units[0]), DEFAULT_SIGHT);
  assert.equal(sightRadius(g, g.units[1]), 6, "cavalry 5 + hill");
});

test("forests block the view; own villages light up their surroundings", () => {
  const map = plainMap(12, 8, { "4,3": "forest", "9,1": "village" });
  map.get({ q: 9, r: 1 }).owner = "red";
  const seen = viewFrom(map, { q: 2, r: 3 }, 4);
  assert.ok(seen.has("3,3") && seen.has("4,3"), "the forest itself is seen");
  assert.ok(!seen.has("6,3"), "but not what is behind it");
  const g = fogArena([["spearman", "red", 2, 3]], map);
  g.villages = [{ q: 9, r: 1 }];
  g.updateVision();
  const vis = visibleHexes(g, "red");
  assert.ok(vis.has("9,1") && vis.has("10,1"));
});

test("hidden enemies cannot be targeted, are ignored by movement and show up in hiddenEnemies", () => {
  const map = plainMap(12, 8, { "4,3": "forest" });
  const g = fogArena([["archer", "red", 2, 3], ["swordsman", "blue", 5, 3], ["spearman", "blue", 3, 1]], map);
  const [ar, hiddenSw, seenSp] = g.units;
  assert.equal(g.isVisible("red", hiddenSw), false);
  assert.equal(g.isVisible("red", seenSp), true);
  assert.deepEqual(hiddenEnemies(g, "red", g.visible("red")).map((u) => u.id), [hiddenSw.id]);
  assert.equal(g.attackPlan(ar, hiddenSw), null);
  assert.ok(!g.targets(ar).includes(hiddenSw));
  assert.equal(hiddenEnemies(g, "red", null).length, 0, "no fog, nobody hidden");
  // explored memory keeps what was seen
  assert.ok(g.isExplored("red", { q: 3, r: 3 }));
  assert.equal(g.isExplored("red", { q: 11, r: 7 }), false);
});

test("walking into a hidden enemy's zone of control springs an ambush", () => {
  const g = fogArena([["cavalry", "red", 1, 3], ["spearman", "blue", 8, 3]], plainMap(14, 8));
  const [cav, sp] = g.units;
  assert.equal(g.isVisible("red", sp), false, "7 hexes away, cavalry sees 5");
  const area = g.area(cav);
  assert.ok(area.get("8,3")?.canStop, "the planner does not know about the spearman");
  const route = g.move(cav, { q: 9, r: 3 });
  const end = route.at(-1);
  assert.equal(key(end), "7,3", "stopped on the first hex next to it");
  assert.equal(cav.mp, 0);
  assert.equal(g.canUndo(), false, "an ambush cannot be undone");
  assert.ok(g.log.some((l) => /Ambush/.test(l.text)));
  assert.ok(g.isVisible("red", sp), "now it is revealed");
});

test("remember merges sets; fog state survives a save round trip", () => {
  assert.deepEqual([...remember(new Set(["a"]), new Set(["b"]))].sort(), ["a", "b"]);
  const g = Game.create({ seed: 4, rules: { fog: true } });
  const n = g.explored[0].size;
  assert.ok(n > 10);
  const back = Game.fromJSON(JSON.parse(JSON.stringify(g.toJSON())));
  assert.equal(back.explored[0].size, n);
  assert.equal(back.rules.fog, true);
});

test("the AI only reacts to enemies it can see and still finishes fogged battles", () => {
  const g = Game.create({ seed: 3, symmetric: true, rules: { fog: true, turnLimit: 12 } });
  const ais = { red: new AIPlayer("red", { seed: 1 }), blue: new AIPlayer("blue", { seed: 2 }) };
  const ctx = ais.red.context(g);
  for (const f of ctx.foes) assert.ok(g.isVisible("red", f));
  for (let i = 0; i < 40 && !g.winner; i++) ais[g.side].playTurn(g);
  assert.ok(g.winner, "decided by the turn limit at the latest");
});
