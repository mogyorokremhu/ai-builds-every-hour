import { test } from "node:test";
import assert from "node:assert/strict";
import { TouchGestures, clampZoom } from "../src/touch.js";

test("quick press without movement is a tap", () => {
  const g = new TouchGestures();
  g.down(1, 50, 50, 0);
  assert.deepEqual(g.up(1, 52, 51, 120), { type: "tap", x: 52, y: 51 });
});

test("long press is reported once", () => {
  const g = new TouchGestures();
  g.down(1, 10, 10, 0);
  assert.equal(g.up(1, 10, 10, 700).type, "longpress");
});

test("dragging past the slop pans and suppresses the tap", () => {
  const g = new TouchGestures();
  g.down(1, 0, 0, 0);
  assert.equal(g.move(1, 3, 0), null);
  assert.deepEqual(g.move(1, 30, 0), { type: "pan", dx: 27, dy: 0 });
  assert.equal(g.up(1, 30, 0, 100), null);
});

test("two fingers pinch with a distance ratio and never tap", () => {
  const g = new TouchGestures();
  g.down(1, 0, 0, 0); g.down(2, 100, 0, 5);
  const r = g.move(2, 200, 0);
  assert.equal(r.type, "pinch");
  assert.equal(r.factor, 2);
  g.up(2, 200, 0, 50);
  assert.equal(g.up(1, 0, 0, 60), null);
});

test("clampZoom keeps zoom in range", () => {
  assert.equal(clampZoom(1, 10), 3);
  assert.equal(clampZoom(1, 0.01), 0.5);
});
