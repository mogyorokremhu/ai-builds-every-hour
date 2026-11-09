import { test } from "node:test";
import assert from "node:assert/strict";
import { installAbilityFx, volleyVictims } from "../src/abilityfxlive.js";

class FakeGame {
  constructor() { this.units = [{ id: 1, side: 0, q: 0, r: 0 }, { id: 2, side: 1, q: 1, r: 0 }, { id: 3, side: 0, q: 2, r: 0 }]; }
  unitAt(h) { return this.units.find((u) => u.q === h.q && u.r === h.r); }
  useAbility(u, id, t) { return { ok: true, id }; }
}

test("wrapper queues effects and returns the original result", () => {
  const ctl = installAbilityFx(FakeGame, () => 1000);
  const g = new FakeGame();
  const res = g.useAbility(g.units[0], "fireball", { q: 1, r: 0 });
  assert.deepEqual(res, { ok: true, id: "fireball" });
  assert.equal(ctl.list.length, 7);
  assert.ok(ctl.list.every((f) => f.start >= 1000));
  ctl.uninstall();
});

test("prune drops finished effects; self-target abilities use the caster hex", () => {
  const ctl = installAbilityFx(FakeGame, () => 0);
  const g = new FakeGame();
  g.useAbility(g.units[0], "shieldwall");
  assert.equal(ctl.list.length, 7);
  assert.ok(ctl.active(100));
  assert.equal(ctl.prune(5000), 0);
  ctl.uninstall();
});

test("volley victims are the target plus adjacent enemies only", () => {
  const g = new FakeGame();
  g.units.push({ id: 4, side: 1, q: 1, r: -1 });
  const v = volleyVictims(g, g.units[0], { q: 1, r: 0 });
  assert.equal(v.length, 2);
});

test("uninstall restores the original method", () => {
  const orig = FakeGame.prototype.useAbility;
  const ctl = installAbilityFx(FakeGame);
  assert.notEqual(FakeGame.prototype.useAbility, orig);
  ctl.uninstall();
  assert.equal(FakeGame.prototype.useAbility, orig);
});
