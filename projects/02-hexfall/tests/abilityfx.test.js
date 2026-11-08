import { test } from "node:test";
import assert from "node:assert/strict";
import { abilityEffects, progress } from "../src/abilityfx.js";

test("volley rains arrows on every victim, deterministic by seed", () => {
  const info = { id: "volley", target: { q: 2, r: 1 }, victims: [{ q: 2, r: 1 }, { q: 3, r: 1 }] };
  const a = abilityEffects(info, 0, 5), b = abilityEffects(info, 0, 5);
  assert.equal(a.length, 14);
  assert.deepEqual(a, b);
  assert.ok(a.every((f) => f.kind === "arrow"));
});

test("fireball bursts at the centre and the six neighbours", () => {
  const fx = abilityEffects({ id: "fireball", target: { q: 0, r: 0 } }, 100);
  assert.equal(fx.length, 7);
  assert.equal(fx.filter((f) => f.ring === 0).length, 1);
  assert.ok(fx.every((f) => f.start >= 100));
});

test("shield wall pulses cover the unit and neighbours; unknown ability gives nothing", () => {
  assert.equal(abilityEffects({ id: "shieldwall", target: { q: 0, r: 0 } }, 0).length, 7);
  assert.deepEqual(abilityEffects({ id: "charge", target: { q: 0, r: 0 } }, 0), []);
});

test("progress is null outside the window", () => {
  const f = { start: 100, duration: 100 };
  assert.equal(progress(f, 50), null);
  assert.equal(progress(f, 150), 0.5);
  assert.equal(progress(f, 250), null);
});
