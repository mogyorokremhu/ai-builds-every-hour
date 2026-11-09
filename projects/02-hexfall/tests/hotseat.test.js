import test from "node:test";
import assert from "node:assert/strict";
import { humanCount, hotseatActive, Curtain } from "../src/hotseat.js";

test("humanCount counts human controllers", () => {
  assert.equal(humanCount(["human", "human"]), 2);
  assert.equal(humanCount(["human", "hard"]), 1);
  assert.equal(humanCount([null, "easy"]), 1);
});

test("hotseat needs fog and two humans", () => {
  assert.equal(hotseatActive({ fog: true, controllers: ["human", "human"] }), true);
  assert.equal(hotseatActive({ fog: false, controllers: ["human", "human"] }), false);
  assert.equal(hotseatActive({ fog: true, controllers: ["human", "normal"] }), false);
});

test("curtain rises for human next side only, not after a win", () => {
  const c = new Curtain();
  const base = { fog: true, controllers: ["human", "human"], active: 1, turn: 3, winner: null };
  assert.equal(c.arm(base), true);
  assert.equal(c.side, 1);
  assert.match(c.message(["Red", "Blue"]), /Blue/);
  assert.equal(c.reveal(), true);
  assert.equal(c.up, false);
  assert.equal(c.message(["Red", "Blue"]), "");
  assert.equal(c.arm({ ...base, winner: 0 }), false);
  assert.equal(c.arm({ ...base, controllers: ["human", "hard"] }), false);
});
