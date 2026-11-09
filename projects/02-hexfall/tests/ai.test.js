import { test } from "node:test";
import assert from "node:assert/strict";
import { AIPlayer, DIFFICULTY } from "../src/ai.js";
import { threatMap, controlMap, distanceField, strikeMap, asciiField, nearestEnemy } from "../src/influence.js";
import { runMatch, runSeries, formatReport } from "../src/selfplay.js";
import { movementArea } from "../src/movement.js";
import { key, distance } from "../src/hex.js";
import { arena, plainMap } from "./helpers.js";

test("threat map covers what enemies can reach and hit next turn", () => {
  const g = arena([["spearman", "red", 1, 3], ["archer", "blue", 8, 3]]);
  const threat = threatMap(g, "red");
  // archer: 5 MP + range 3 → threatens up to 8 hexes away, not beyond
  assert.ok(threat.get("3,3"), "hex within move + range is threatened");
  assert.equal(threat.get("8,3").count, 1);
  const far = [...g.map].filter((t) => distance(t, { q: 8, r: 3 }) > 8);
  for (const t of far) assert.equal(threat.get(key(t)), undefined);
  const ctl = controlMap(g, "blue");
  assert.ok(ctl.get("8,3") > 0, "blue controls the hexes around its archer");
  assert.ok(asciiField(g, new Map([...threat].map(([k, v]) => [k, v.damage]))).split("\n").length === g.map.rows);
  assert.equal(nearestEnemy(g, g.units[0]).id, 2);
});

test("strike map counts each attacker once per hex", () => {
  const g = arena([["cavalry", "red", 2, 2], ["cavalry", "red", 2, 4]]);
  const m = strikeMap(g, g.units);
  assert.equal(m.get("3,3").count, 2);
  assert.equal(m.get("3,3").damage, 20);
});

test("distance field respects terrain costs and walls", () => {
  const map = plainMap(10, 3, { "4,0": "mountain", "4,1": "mountain", "3,2": "forest" });
  const g = arena([], { map });
  const d = distanceField(g, [{ q: 0, r: 1 }]);
  assert.equal(d.get("0,1"), 0);
  assert.equal(d.get("1,1"), 1);
  assert.equal(d.get("4,1"), undefined, "mountains are never entered");
  assert.ok(d.get("6,1") > 6, "the wall forces a detour");
});

test("the AI finishes off a wounded enemy instead of wandering", () => {
  const g = arena([["swordsman", "red", 3, 3], ["archer", "blue", 5, 3], ["swordsman", "blue", 8, 6]]);
  g.units[1].hp = 6;
  const ai = new AIPlayer("red", { difficulty: "hard" });
  const a = ai.nextAction(g);
  assert.equal(a.type, "attack");
  assert.equal(a.targetId, 2);
  ai.play(g, a);
  assert.equal(g.unitById(2), null, "the archer is dead");
});

test("a badly wounded AI unit falls back to a village to heal", () => {
  const map = plainMap(12, 8, { "1,3": "village" });
  const g = arena([["swordsman", "red", 4, 3], ["swordsman", "blue", 9, 3], ["swordsman", "blue", 9, 5]], { map });
  g.villages = [{ q: 1, r: 3 }];
  g.map.get({ q: 1, r: 3 }).owner = "red";
  g.units[0].hp = 8;
  const ai = new AIPlayer("red", { difficulty: "hard" });
  const a = ai.nextAction(g);
  assert.equal(a.type, "move");
  assert.equal(key(a.to), "1,3");
});

test("the AI grabs a free village in reach", () => {
  const map = plainMap(14, 8, { "5,3": "village" });
  const g = arena([["cavalry", "red", 2, 3], ["spearman", "blue", 12, 6]], { map });
  g.villages = [{ q: 5, r: 3 }];
  const ai = new AIPlayer("red", { difficulty: "hard" });
  const a = ai.nextAction(g);
  assert.equal(a.type, "move");
  assert.equal(key(a.to), "5,3");
});

test("AI turns are legal, end the turn, and are deterministic per seed", () => {
  const play = () => {
    const r = runMatch({ seed: 5, rules: { turnLimit: 6 } });
    return { winner: r.winner, reason: r.reason, turns: r.turns, log: r.game.log.map((l) => l.text) };
  };
  const a = play(), b = play();
  assert.deepEqual(a, b);
  assert.ok(a.winner, "a 6-turn battle is always decided");
  assert.ok(a.log.some((t) => /hits|shoots|blasts/.test(t)), "the armies fought");
});

test("every difficulty plays a full turn; unknown difficulties are refused", async () => {
  const { Game } = await import("../src/game.js");
  for (const d of Object.keys(DIFFICULTY)) {
    const g = Game.create({ seed: 9 });
    const ai = new AIPlayer("red", { difficulty: d, seed: 3 });
    const actions = ai.playTurn(g);
    assert.equal(g.side, "blue", `${d}: turn passed`);
    assert.ok(actions.length >= 2);
    assert.ok(g.unitsOf("red").every((u) => movementArea(g, u)), "units still valid");
  }
  assert.throws(() => new AIPlayer("red", { difficulty: "godlike" }));
});

test("self-play series aggregates results into a report", () => {
  const s = runSeries({ games: 2, start: 20, rules: { turnLimit: 8 } });
  assert.equal(s.games, 2);
  assert.equal(s.wins.red + s.wins.blue + s.wins.draw + s.wins.none, 2);
  const text = formatReport(s, "test");
  assert.match(text, /2 games/);
  assert.match(text, /wins: red/);
});

test("recruit weights favour mages and healers behind a melee line, rogues less", async () => {
  const { RECRUIT_MIX } = await import("../src/ai.js");
  assert.ok(RECRUIT_MIX.mage > RECRUIT_MIX.rogue);
  assert.ok(RECRUIT_MIX.healer > 1 && RECRUIT_MIX.rogue < RECRUIT_MIX.mage);
});
