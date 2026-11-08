import { test } from "node:test";
import assert from "node:assert/strict";
import * as H from "../src/hex.js";

test("distance and neighbours", () => {
  const o = H.hex(0, 0);
  assert.equal(H.neighbors(o).length, 6);
  for (const n of H.neighbors(o)) assert.equal(H.distance(o, n), 1);
  assert.equal(H.distance(H.hex(0, 0), H.hex(3, -1)), 3);
  assert.equal(H.distance(H.hex(-2, 4), H.hex(2, -1)), 5);
});

test("keys round-trip", () => {
  const h = H.hex(-3, 7);
  assert.deepEqual(H.fromKey(H.key(h)), h);
});

test("rings and spirals have the right sizes", () => {
  for (let r = 0; r < 6; r++) {
    const ring = H.ring(H.hex(2, -1), r);
    assert.equal(ring.length, r === 0 ? 1 : 6 * r);
    for (const h of ring) assert.equal(H.distance(h, H.hex(2, -1)), r);
    assert.equal(new Set(ring.map(H.key)).size, ring.length);
  }
  assert.equal(H.spiral(H.hex(0, 0), 3).length, 1 + 6 + 12 + 18);
});

test("lines are contiguous and the right length", () => {
  const a = H.hex(0, 0), b = H.hex(5, -2);
  const l = H.line(a, b);
  assert.equal(l.length, H.distance(a, b) + 1);
  assert.deepEqual(l[0], a);
  assert.deepEqual(l.at(-1), b);
  for (let i = 1; i < l.length; i++) assert.equal(H.distance(l[i - 1], l[i]), 1);
  assert.deepEqual(H.line(a, a), [a]);
});

test("rounding picks the nearest hex", () => {
  assert.deepEqual(H.round(0.1, 0.1), H.hex(0, 0));
  assert.deepEqual(H.round(0.9, -0.1), H.hex(1, 0));
  assert.deepEqual(H.round(-0.2, -0.2), H.hex(0, 0));
  assert.deepEqual(H.round(-0.4, -0.4), H.hex(0, -1)); // cube (-.4,-.4,.8) is nearer (0,-1,1)
  assert.ok(!Object.is(H.round(-0.2, 0.1).q, -0));
});

test("pixel conversion round-trips", () => {
  for (const h of H.spiral(H.hex(1, 1), 4)) {
    const p = H.toPixel(h, 20);
    assert.deepEqual(H.fromPixel(p.x, p.y, 20), h);
    assert.deepEqual(H.fromPixel(p.x + 7, p.y - 6, 20), h); // inside the hex
  }
  assert.equal(H.corners(0, 0, 10).length, 6);
});

test("offset coordinates round-trip", () => {
  for (let row = 0; row < 6; row++) {
    for (let col = 0; col < 6; col++) {
      const h = H.fromOffset(col, row);
      assert.deepEqual(H.toOffset(h), { col, row });
    }
  }
});

test("rotation", () => {
  const c = H.hex(1, 1);
  const h = H.hex(3, 0);
  assert.deepEqual(H.rotate(h, c, 6), h);
  assert.equal(H.distance(H.rotate(h, c, 1), c), H.distance(h, c));
  assert.deepEqual(H.rotate(H.rotate(h, c, 2), c, -2), h);
  const six = [0, 1, 2, 3, 4, 5].map((k) => H.key(H.rotate(h, c, k)));
  assert.equal(new Set(six).size, 6);
});
