import { test } from "node:test";
import assert from "node:assert/strict";
import { snapshotUnits, diffEffects, effectState, effectsDone, FLOAT_MS } from "../src/effects.js";

const mk = (id, q, hp, side = "red") => ({ id, q, r: 0, hp, side, type: "archer" });

test("no change gives no effects", () => {
  const us = [mk(1, 0, 20), mk(2, 1, 20, "blue")];
  assert.deepEqual(diffEffects(snapshotUnits(us), us, 0), []);
});

test("damage and healing produce signed floating numbers", () => {
  const us = [mk(1, 0, 20), mk(2, 1, 20, "blue")];
  const snap = snapshotUnits(us);
  us[0].hp = 26; us[1].hp = 11;
  const fx = diffEffects(snap, us, 100);
  assert.equal(fx.length, 2);
  assert.deepEqual(fx.map((f) => f.text).sort(), ["+6", "-9"]);
  assert.ok(fx.find((f) => f.text === "+6").heal);
});

test("a dead unit gets a number and a fade at its old hex", () => {
  const us = [mk(1, 0, 20), mk(2, 1, 5, "blue")];
  const snap = snapshotUnits(us);
  const fx = diffEffects(snap, [us[0]], 0);
  assert.equal(fx.length, 2);
  const fade = fx.find((f) => f.kind === "fade");
  assert.deepEqual(fade.at, { q: 1, r: 0 });
  assert.equal(fx.find((f) => f.kind === "float").text, "-5");
});

test("stacked numbers on one hex are staggered", () => {
  const a = mk(1, 0, 10), b = mk(2, 0, 10);
  const snap = snapshotUnits([a, b]);
  a.hp = 5; b.hp = 4;
  const fx = diffEffects(snap, [a, b], 0);
  assert.notEqual(fx[0].start, fx[1].start);
});

test("effect state is null outside its window and fades out", () => {
  const f = { kind: "float", start: 100, duration: FLOAT_MS };
  assert.equal(effectState(f, 50), null);
  assert.equal(effectState(f, 100 + FLOAT_MS + 1), null);
  assert.equal(effectState(f, 100 + FLOAT_MS * 0.99).alpha < 0.1, true);
  const d = { kind: "fade", start: 0, duration: 500 };
  assert.ok(effectState(d, 250).alpha > 0.4 && effectState(d, 250).alpha < 0.6);
  assert.ok(effectsDone([f, d], 5000));
  assert.ok(!effectsDone([f, d], 200));
});
