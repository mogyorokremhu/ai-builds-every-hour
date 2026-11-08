import test from "node:test";
import assert from "node:assert/strict";
import { Game } from "../src/game.js";
import { installShowAll, guardAI } from "../src/showall.js";
import { arena } from "./helpers.js";

const fogGame = () => { const g = arena([["spearman", 0, 0, 0], ["spearman", 1, 4, 7]]); g.rules.fog = true; return g; };

test("show-all reveals far enemies, off restores fog", () => {
  const ctl = installShowAll(Game, null);
  try {
    const g = fogGame();
    const far = g.units[1];
    assert.equal(g.isVisible(0, far), false);
    ctl.showAll = true;
    assert.equal(g.isVisible(0, far), true);
    assert.ok(g.visible(0).has(`${far.q},${far.r}`));
    ctl.showAll = false;
    assert.equal(g.isVisible(0, far), false);
  } finally { ctl.uninstall(); }
});

test("AI calls are guarded: no free vision while thinking", () => {
  class FakeAI { peek(g, u) { return g.isVisible(0, u); } }
  const ctl = installShowAll(Game, FakeAI);
  try {
    const g = fogGame();
    ctl.showAll = true;
    assert.equal(new FakeAI().peek(g, g.units[1]), false);
    assert.equal(g.isVisible(0, g.units[1]), true);
    assert.equal(ctl.depth, 0);
  } finally { ctl.uninstall(); }
});

test("guard resets depth after a throw and is idempotent", () => {
  class A { boom() { throw new Error("x"); } }
  const ctl = { depth: 0 };
  guardAI(A, ctl); guardAI(A, ctl);
  assert.throws(() => new A().boom());
  assert.equal(ctl.depth, 0);
});

test("fog off: visible stays null", () => {
  const ctl = installShowAll(Game, null);
  try { const g = arena([["spearman", 0, 0, 0]]); ctl.showAll = true; assert.equal(g.visible(0), null); } finally { ctl.uninstall(); }
});
