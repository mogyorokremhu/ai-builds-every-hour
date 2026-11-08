// Visual effects derived from state changes: floating damage/heal numbers and death fades.
// Pure helpers (no DOM) except drawEffects, which only needs a 2D context.
import { hexCenter } from "./render.js";
import { unitType } from "./units.js";

export const FLOAT_MS = 900;
export const FADE_MS = 700;

/** Remember HP, position and look of every unit so a later diff can tell what changed. */
export function snapshotUnits(units) {
  return new Map(units.map((u) => [u.id, { id: u.id, q: u.q, r: u.r, hp: u.hp, side: u.side, type: u.type }]));
}

/**
 * Compare a snapshot with the units now alive and return effects:
 * a floating number for every HP change and a fade for every unit that vanished.
 * Several numbers on one hex are staggered so they stay readable.
 */
export function diffEffects(before, unitsAfter, start) {
  const alive = new Map(unitsAfter.map((u) => [u.id, u]));
  const fx = [];
  const stack = new Map();
  for (const [id, old] of before) {
    const now = alive.get(id);
    const delta = (now ? now.hp : 0) - old.hp;
    if (delta === 0 && now) continue;
    const at = now ?? old;
    const k = `${at.q},${at.r}`;
    const n = stack.get(k) ?? 0;
    stack.set(k, n + 1);
    if (delta !== 0) {
      fx.push({ kind: "float", at: { q: at.q, r: at.r }, text: delta > 0 ? `+${delta}` : `${delta}`, heal: delta > 0, start: start + n * 180, duration: FLOAT_MS });
    }
    if (!now) fx.push({ kind: "fade", at: { q: old.q, r: old.r }, side: old.side, type: old.type, start, duration: FADE_MS });
  }
  return fx;
}

/** Style of an effect at time `now`: alpha 0..1 plus a rise/shrink amount, or null if not active. */
export function effectState(fx, now) {
  const t = (now - fx.start) / fx.duration;
  if (t < 0 || t > 1) return null;
  if (fx.kind === "float") return { alpha: t < 0.6 ? 1 : 1 - (t - 0.6) / 0.4, rise: t, scale: 1 + 0.35 * Math.sin(Math.PI * Math.min(1, t * 2.5)) };
  return { alpha: 1 - t, rise: 0, scale: 1 - 0.25 * t };
}

export const effectsDone = (list, now) => list.every((e) => now >= e.start + e.duration);

export function drawEffects(ctx, list, now, layout, sideColors = {}) {
  const s = layout.size;
  for (const fx of list) {
    const st = effectState(fx, now);
    if (!st) continue;
    const c = hexCenter(fx.at, layout);
    ctx.save();
    ctx.globalAlpha = st.alpha;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    if (fx.kind === "fade") {
      const r = s * 0.55 * st.scale;
      ctx.fillStyle = sideColors[fx.side] ?? "#888";
      ctx.beginPath();
      ctx.arc(c.x, c.y, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#fff";
      ctx.font = `bold ${Math.round(r * 1.05)}px system-ui, sans-serif`;
      ctx.fillText(unitType(fx).glyph, c.x, c.y + 1);
    } else {
      ctx.font = `bold ${Math.round(s * 0.7 * st.scale)}px system-ui, sans-serif`;
      ctx.lineWidth = Math.max(2, s / 6);
      ctx.strokeStyle = "#15181c";
      ctx.fillStyle = fx.heal ? "#7ddc6a" : "#ff6b5a";
      const y = c.y - s * 0.5 - st.rise * s * 0.9;
      ctx.strokeText(fx.text, c.x, y);
      ctx.fillText(fx.text, c.x, y);
    }
    ctx.restore();
  }
}
