import { test } from "node:test";
import assert from "node:assert/strict";
import { CYCLE, timeOfDay, alignmentBonus, todMultiplier, upcoming } from "../src/timeofday.js";
import { damageRolls, strikeModifiers } from "../src/combat.js";
import { UNIT_TYPES } from "../src/units.js";
import { arena } from "./helpers.js";

test("the cycle repeats every six turns starting at dawn", () => {
  assert.equal(CYCLE.length, 6);
  assert.equal(timeOfDay(1).id, "dawn");
  assert.equal(timeOfDay(2).id, "morning");
  assert.equal(timeOfDay(5).id, "first-watch");
  assert.equal(timeOfDay(7).id, "dawn");
  assert.equal(timeOfDay(0).id, "second-watch");
  assert.deepEqual(upcoming(3, 3).map((p) => [p.turn, p.id]), [[3, "afternoon"], [4, "dusk"], [5, "first-watch"]]);
});

test("lawful units gain by day, chaotic by night, neutral never", () => {
  const day = timeOfDay(2), night = timeOfDay(5);
  assert.equal(alignmentBonus("lawful", day), 25);
  assert.equal(alignmentBonus("chaotic", day), -25);
  assert.equal(alignmentBonus("chaotic", night), 25);
  assert.equal(alignmentBonus("neutral", night), 0);
  assert.equal(todMultiplier("lawful", 5), 0.75);
  for (const t of Object.values(UNIT_TYPES)) assert.ok(["lawful", "neutral", "chaotic"].includes(t.alignment), t.id);
});

test("combat damage follows the time of day", () => {
  const g = arena([["swordsman", "red", 3, 3], ["rogue", "blue", 4, 3]]);
  const [sw, rogue] = g.units;
  const at = (turn) => {
    g.turn = turn;
    return { sword: damageRolls(g, sw, rogue, "melee")[2], rogue: damageRolls(g, rogue, sw, "melee")[2] };
  };
  const dawn = at(1), noon = at(2), night = at(5);
  assert.ok(noon.sword > dawn.sword && dawn.sword > night.sword);
  assert.ok(night.rogue > dawn.rogue && dawn.rogue > noon.rogue);
  g.turn = 2;
  assert.equal(strikeModifiers(g, sw, rogue, "melee").time, 1.25);
});
