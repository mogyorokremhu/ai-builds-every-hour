import { test } from "node:test";
import assert from "node:assert/strict";
import { camera, view, zoomAt, panBy, clamp, visibleRect, centerOn, MAX_ZOOM } from "../src/camera.js";
import { fitLayout, hexCenter, hexAtPixel } from "../src/render.js";
import { HexMap } from "../src/map.js";
import { fromOffset, key } from "../src/hex.js";

const vp = { width: 800, height: 520 };
const map = new HexMap(24, 16);
const base = fitLayout(map, vp.width, vp.height);

test("fitLayout fits the whole map in the viewport", () => {
  for (const t of map) {
    const c = hexCenter(t, base);
    assert.ok(c.x - base.size >= 0 && c.x + base.size <= vp.width + 1, `x out at ${key(t)}`);
    assert.ok(c.y - base.size >= 0 && c.y + base.size <= vp.height + 1, `y out at ${key(t)}`);
  }
  const h = fromOffset(5, 7);
  const c = hexCenter(h, base);
  assert.deepEqual(hexAtPixel(c.x, c.y, base), h);
});

test("zoom keeps the point under the cursor fixed", () => {
  const cam = camera(base);
  const target = fromOffset(10, 6);
  const before = hexCenter(target, view(cam));
  const z = zoomAt(cam, 2, before.x, before.y);
  const after = hexCenter(target, view(z));
  assert.ok(Math.abs(after.x - before.x) < 1e-6 && Math.abs(after.y - before.y) < 1e-6);
  assert.equal(z.zoom, 2);
  assert.equal(zoomAt(z, 100, 0, 0).zoom, MAX_ZOOM);
  assert.equal(zoomAt(cam, 0.1, 0, 0).zoom, 1);
});

test("panning is clamped to the map", () => {
  let cam = camera(base);
  cam = panBy(cam, 300, 300, vp);
  assert.deepEqual([cam.panX, cam.panY], [0, 0]); // zoom 1: no panning
  cam = zoomAt(cam, 2, 400, 260, vp);
  cam = panBy(cam, -5000, -5000, vp);
  assert.equal(cam.panX, vp.width - vp.width * 2);
  assert.equal(cam.panY, vp.height - vp.height * 2);
  const r = visibleRect(cam, vp);
  assert.equal(r.w, 400);
  assert.equal(r.x + r.w, vp.width); // showing the bottom-right quarter
  const centred = centerOn(cam, 400, 260, vp);
  const rc = visibleRect(centred, vp);
  assert.equal(rc.x + rc.w / 2, 400);
  assert.deepEqual(clamp({ ...cam, panX: 50, panY: 50 }, vp).panX, 0);
});
