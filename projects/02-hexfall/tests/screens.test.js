import { test } from "node:test";
import assert from "node:assert/strict";
import { skirmishHtml, readSkirmishForm, campaignHtml, loadProgress, saveProgress } from "../src/screens.js";
import { MemoryStorage } from "../src/save.js";
import { toGameOptions } from "../src/skirmish.js";
import { Game } from "../src/game.js";
import { newProgress } from "../src/campaign.js";

test("skirmish form lists every field and round-trips through the parser", () => {
  const html = skirmishHtml({ seed: 7, size: "large", fog: true });
  for (const id of ["seed", "size", "army0", "army1", "redai", "blueai", "gold", "turns", "fog", "weather", "sym", "start"]) {
    assert.ok(html.includes(`id="sk-${id}"`), id);
  }
  assert.match(html, /<option value="large" selected>/);
  const { setup, ai } = readSkirmishForm({ seed: "42", size: "small", army0: "cavalry", army1: "ranged", fog: true, gold: "999", turns: "x", redai: "hard", blueai: "bogus" });
  assert.equal(setup.seed, 42);
  assert.equal(setup.startGold, 500);
  assert.equal(setup.turnLimit, 0);
  assert.equal(ai.red, "hard");
  assert.equal(ai.blue, "normal");
  assert.ok(Game.create(toGameOptions(setup)).unitsOf("red").length >= 1);
});

test("oversized armies on small maps show a warning", () => {
  assert.match(skirmishHtml({ size: "small", armies: ["ranged", "standard"] }), /class="problems"/);
});

test("campaign menu marks done / current / locked", () => {
  const html = campaignHtml({ ...newProgress(), index: 2, won: 2 });
  assert.equal((html.match(/class="sc done"/g) || []).length, 2);
  assert.equal((html.match(/class="sc current"/g) || []).length, 1);
  assert.equal((html.match(/class="sc locked"/g) || []).length, 2);
  assert.match(html, /Continue/);
  assert.match(campaignHtml({ ...newProgress(), index: 5 }), /Campaign complete/);
});

test("progress persists and survives corrupt storage", () => {
  const s = new MemoryStorage();
  assert.equal(loadProgress(s).index, 0);
  saveProgress(s, { index: 3, roster: [], won: 3, lost: 1 });
  assert.equal(loadProgress(s).index, 3);
  s.setItem("hexfall.campaign", "{oops");
  assert.equal(loadProgress(s).index, 0);
});
