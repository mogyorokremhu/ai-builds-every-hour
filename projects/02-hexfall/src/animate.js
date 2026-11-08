// Pure animation helpers: tweening units along routes and short attack lunges.
import { hexCenter } from "./render.js";

export const MS_PER_HEX = 110;
export const LUNGE_MS = 260;

/** Smooth start and stop (cubic ease in/out) for t in [0, 1]. */
export function easeInOut(t) {
  const x = Math.min(1, Math.max(0, t));
  return x < 0.5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2;
}

/** A movement animation for `unitId` along `route` (hexes) starting at time `start` (ms). */
export function moveAnimation(unitId, route, start, msPerHex = MS_PER_HEX) {
  return { kind: "move", unitId, route, start, duration: Math.max(1, (route.length - 1) * msPerHex) };
}

/** A lunge: the attacker darts 35% of the way towards the target and back. */
export function lungeAnimation(unitId, from, to, start, duration = LUNGE_MS) {
  return { kind: "lunge", unitId, from, to, start, duration };
}

/** Fraction of `anim` done at time `now` (0..1). */
export function progress(anim, now) {
  return Math.min(1, Math.max(0, (now - anim.start) / anim.duration));
}

export function finished(anim, now) {
  return now >= anim.start + anim.duration;
}

/**
 * Pixel position of the animated unit at time `now`.
 * Moves ease over the whole route (constant speed between hex centres in between).
 */
export function animatedPosition(anim, now, layout) {
  const t = progress(anim, now);
  if (anim.kind === "lunge") {
    const a = hexCenter(anim.from, layout), b = hexCenter(anim.to, layout);
    const k = Math.sin(Math.PI * t) * 0.35;
    return { x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k };
  }
  const pts = anim.route.map((h) => hexCenter(h, layout));
  if (pts.length === 1) return pts[0];
  const f = easeInOut(t) * (pts.length - 1);
  const i = Math.min(pts.length - 2, Math.floor(f));
  const u = f - i;
  return { x: pts[i].x + (pts[i + 1].x - pts[i].x) * u, y: pts[i].y + (pts[i + 1].y - pts[i].y) * u };
}
