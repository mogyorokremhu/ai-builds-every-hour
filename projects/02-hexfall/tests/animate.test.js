import { test } from "node:test";
import assert from "node:assert/strict";
import { easeInOut, moveAnimation, lungeAnimation, animatedPosition, progress, finished, MS_PER_HEX } from "../src/animate.js";
import { hexCenter } from "../src/render.js";

const layout = { size: 20, ox: 30, oy: 30 };
const route = [{ q: 0, r: 0 }, { q: 1, r: 0 }, { q: 2, r: 0 }];

test("easing is monotonic from 0 to 1 and symmetric", () => {
  assert.equal(easeInOut(0), 0);
  assert.equal(easeInOut(1), 1);
  assert.equal(easeInOut(-3), 0);
  assert.equal(easeInOut(7), 1);
  let prev = 0;
  for (let i = 1; i <= 100; i++) {
    const v = easeInOut(i / 100);
    assert.ok(v >= prev);
    prev = v;
  }
  assert.ok(Math.abs(easeInOut(0.3) + easeInOut(0.7) - 1) < 1e-12);
});

test("move animation starts and ends on hex centres and passes the middle", () => {
  const a = moveAnimation(7, route, 1000);
  assert.equal(a.duration, 2 * MS_PER_HEX);
  assert.deepEqual(animatedPosition(a, 1000, layout), hexCenter(route[0], layout));
  assert.deepEqual(animatedPosition(a, 5000, layout), hexCenter(route[2], layout));
  const mid = animatedPosition(a, 1000 + a.duration / 2, layout);
  const c = hexCenter(route[1], layout);
  assert.ok(Math.abs(mid.x - c.x) < 1e-9 && Math.abs(mid.y - c.y) < 1e-9);
  assert.equal(progress(a, 0), 0);
  assert.ok(!finished(a, 1100) && finished(a, 1000 + a.duration));
});

test("single-hex route stays put", () => {
  const a = moveAnimation(1, [route[0]], 0);
  assert.deepEqual(animatedPosition(a, 50, layout), hexCenter(route[0], layout));
});

test("lunge goes out and comes back", () => {
  const a = lungeAnimation(1, route[0], route[1], 0, 200);
  const start = animatedPosition(a, 0, layout), peak = animatedPosition(a, 100, layout), end = animatedPosition(a, 200, layout);
  const from = hexCenter(route[0], layout), to = hexCenter(route[1], layout);
  assert.ok(Math.abs(start.x - from.x) < 1e-9 && Math.abs(end.x - from.x) < 1e-9);
  assert.ok(Math.abs(peak.x - (from.x + (to.x - from.x) * 0.35)) < 1e-9);
});
