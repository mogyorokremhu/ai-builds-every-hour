import { test } from "node:test";
import assert from "node:assert/strict";
import { WEATHER, FRONT_LENGTH, weatherFor, currentWeather, weatherForecast, hash2 } from "../src/weather.js";
import { damageRolls, effectiveRange, attackKind } from "../src/combat.js";
import { sightRadius } from "../src/fog.js";
import { arena } from "./helpers.js";

/** Find a seed whose second front has the weather `id` (turns 4–6). */
function seedWith(id) {
  for (let s = 1; s < 5000; s++) if (weatherFor(s, FRONT_LENGTH + 1).id === id) return s;
  throw new Error(`no seed with ${id}`);
}

test("the first front is always clear; fronts last FRONT_LENGTH turns; deterministic", () => {
  for (let s = 1; s < 50; s++) {
    for (let t = 1; t <= FRONT_LENGTH; t++) assert.equal(weatherFor(s, t).id, "clear");
    assert.equal(weatherFor(s, 4), weatherFor(s, 6));
    assert.equal(weatherFor(s, 10), weatherFor(s, 10));
  }
  assert.equal(hash2(3, 4), hash2(3, 4));
  assert.notEqual(hash2(3, 4), hash2(4, 3));
});

test("all four weathers occur with roughly the configured weights", () => {
  const counts = { clear: 0, rain: 0, fog: 0, storm: 0 };
  for (let s = 1; s <= 400; s++) for (let f = 1; f <= 5; f++) counts[weatherFor(s, f * FRONT_LENGTH + 1).id] += 1;
  const n = 2000;
  assert.ok(counts.clear / n > 0.4 && counts.clear / n < 0.6, JSON.stringify(counts));
  assert.ok(counts.storm > 100 && counts.rain > counts.storm);
});

test("rain weakens arrows, fog shortens reach and sight; the weather rule can be turned off", () => {
  const g = arena([["archer", "red", 2, 3], ["swordsman", "blue", 5, 3]]);
  const [ar, sw] = g.units;
  const clear = damageRolls(g, ar, sw, "ranged")[2];
  assert.equal(effectiveRange(g, ar), 3);
  g.seed = seedWith("rain");
  g.turn = FRONT_LENGTH + 1;
  assert.equal(currentWeather(g).id, "rain");
  assert.ok(damageRolls(g, ar, sw, "ranged")[2] < clear);
  assert.equal(damageRolls(g, sw, ar, "melee")[2], (() => { g.rules.weather = false; const d = damageRolls(g, sw, ar, "melee")[2]; g.rules.weather = true; return d; })(), "melee is unaffected");
  g.seed = seedWith("fog");
  assert.equal(effectiveRange(g, ar), 2);
  assert.equal(attackKind(g, ar, sw), null, "3 hexes is out of reach in fog");
  assert.equal(sightRadius(g, ar), WEATHER.fog.sightPenalty ? 5 - 2 : 5);
  g.rules.weather = false;
  assert.equal(currentWeather(g).id, "clear");
  assert.equal(effectiveRange(g, ar), 3);
});

test("forecast lists the coming turns", () => {
  const g = arena([]);
  g.seed = 99;
  const f = weatherForecast(g, 8);
  assert.equal(f.length, 8);
  assert.deepEqual(f.map((x) => x.turn), [1, 2, 3, 4, 5, 6, 7, 8]);
  assert.equal(f[3].id, weatherFor(99, 4).id);
});

test("rain puts out fires at the start of a round", () => {
  const g = arena([["spearman", "red", 1, 1], ["spearman", "blue", 8, 6]]);
  g.seed = seedWith("rain");
  g.turn = FRONT_LENGTH; // the next round starts a rainy front
  g.map.get({ q: 4, r: 3 }).fire = 3;
  g.endTurn();
  g.endTurn();
  assert.equal(g.turn, FRONT_LENGTH + 1);
  assert.equal(g.map.burning().length, 0);
  assert.ok(g.log.some((l) => /puts out/.test(l.text)));
});
