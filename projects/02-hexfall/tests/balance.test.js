import test from "node:test";
import assert from "node:assert/strict";
import { unitEfficiency, sideBias, balanceFlags, balanceMarkdown } from "../src/balance.js";

const series = (over = {}) => ({
  games: 20, avgTurns: 12, wins: { red: 10, blue: 10, draw: 0, none: 0 }, reasons: { hold: 20 },
  recruits: { spearman: 10, swordsman: 10, archer: 10, cavalry: 10, mage: 10, healer: 10, rogue: 10 },
  kills: { spearman: 10, swordsman: 10, archer: 10, cavalry: 10, mage: 10, healer: 10, rogue: 10 },
  abilities: { heal: 3 }, ...over,
});

test("efficiency divides kills by recruits and gold", () => {
  const row = unitEfficiency(series()).find((r) => r.id === "spearman");
  assert.equal(row.perRecruit, 1);
  assert.ok(Math.abs(row.per100Gold - (10 / 140) * 100) < 1e-9);
});

test("sideBias is neutral for an even split and large for a sweep", () => {
  assert.equal(sideBias(series()).z, 0);
  assert.ok(sideBias(series({ wins: { red: 18, blue: 2, draw: 0, none: 0 } })).z > 1.96);
  assert.equal(sideBias(series({ wins: { red: 0, blue: 0, draw: 0, none: 0 } })).redShare, 0.5);
});

test("flags catch outliers, unused units, bias and timeouts", () => {
  const f = balanceFlags(series({
    kills: { spearman: 10, swordsman: 10, archer: 10, cavalry: 10, mage: 100, healer: 0, rogue: 10 },
    recruits: { spearman: 10, swordsman: 10, archer: 10, cavalry: 10, mage: 10, healer: 0, rogue: 10 },
    wins: { red: 19, blue: 1, draw: 0, none: 0 }, reasons: { turns: 8, hold: 12 },
  }));
  assert.ok(f.some((x) => /Mage overperforms/.test(x)));
  assert.ok(f.some((x) => /Healer was never recruited/.test(x)));
  assert.ok(f.some((x) => /side bias/.test(x)));
  assert.ok(f.some((x) => /turn limit/.test(x)));
  assert.deepEqual(balanceFlags(series()), []);
});

test("markdown contains a table row per unit", () => {
  const md = balanceMarkdown(series(), "Test");
  assert.match(md, /### Test/);
  assert.equal(md.split("\n").filter((l) => l.startsWith("| ") && !l.includes("Unit")).length, 7);
});
