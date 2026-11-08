// Touch gesture recogniser (pure logic): feed pointer events, get tap / pan / pinch / long-press results.
// main.js can map: tap = click, pan = camera drag, pinch = zoom, long-press = inspect (right-click).
export const TAP_MAX_MS = 300;
export const TAP_SLOP = 10;
export const LONG_MS = 500;

export class TouchGestures {
  constructor() { this.pts = new Map(); this.start = null; this.moved = false; this.lastPinch = null; this.multi = false; }

  down(id, x, y, t) {
    this.pts.set(id, { x, y });
    if (this.pts.size === 1) { this.start = { x, y, t }; this.moved = false; this.multi = false; }
    else { this.multi = true; this.lastPinch = this.#dist(); }
    return null;
  }

  move(id, x, y) {
    const p = this.pts.get(id);
    if (!p) return null;
    const dx = x - p.x, dy = y - p.y;
    p.x = x; p.y = y;
    if (this.pts.size >= 2) {
      const d = this.#dist(), prev = this.lastPinch;
      this.lastPinch = d;
      return prev && d ? { type: "pinch", factor: d / prev } : null;
    }
    if (this.start && Math.hypot(x - this.start.x, y - this.start.y) > TAP_SLOP) this.moved = true;
    return this.moved ? { type: "pan", dx, dy } : null;
  }

  up(id, x, y, t) {
    this.pts.delete(id);
    if (this.pts.size > 0) { this.lastPinch = this.pts.size >= 2 ? this.#dist() : null; return null; }
    const s = this.start; this.start = null; this.lastPinch = null;
    if (!s || this.moved || this.multi) return null;
    const held = t - s.t;
    if (held >= LONG_MS) return { type: "longpress", x, y };
    return held <= TAP_MAX_MS ? { type: "tap", x, y } : null;
  }

  cancel() { this.pts.clear(); this.start = null; this.lastPinch = null; this.moved = false; this.multi = false; }

  #dist() {
    const [a, b] = [...this.pts.values()];
    return a && b ? Math.hypot(a.x - b.x, a.y - b.y) : 0;
  }
}

/** Clamp a zoom factor so the camera size stays in range. */
export const clampZoom = (current, factor, min = 0.5, max = 3) => Math.min(max, Math.max(min, current * factor));
