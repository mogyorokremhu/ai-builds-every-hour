import test from "node:test";
import assert from "node:assert/strict";
import { pinchSteps, WHEEL_STEP } from "../src/pinch.js";

test("small pinch accumulates without stepping", () => {
  const r = pinchSteps(0, 1.05);
  assert.equal(r.steps, 0);
  assert.ok(r.acc > 0);
});
test("accumulated pinch crosses a step", () => {
  let r = pinchSteps(0, 1.1);
  r = pinchSteps(r.acc, 1.1);
  assert.equal(r.steps, 1);
});
test("pinch out gives negative steps", () => {
  assert.equal(pinchSteps(0, 1 / (WHEEL_STEP * WHEEL_STEP * 1.01)).steps, -2);
});
test("bad factor is ignored", () => {
  assert.deepEqual(pinchSteps(0.2, 0), { steps: 0, acc: 0.2 });
});
