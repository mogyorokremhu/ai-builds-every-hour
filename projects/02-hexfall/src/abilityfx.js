// Ability animations: arrow rain (volley), fireball burst, heal sparkles, shield/rally pulses.
// Pure builders (deterministic via seed) + a canvas drawer. Same effect shape as effects.js
// ({kind, at, start, duration}) so main.js can mix both lists.
import { hexCenter } from "./render.js";
import { neighbors } from "./hex.js";
import { RNG } from "./rng.js";

export const ARROW_MS = 700;
export const BURST_MS = 650;
export const PULSE_MS = 600;

/** Build the effect list for one ability use. `info` = { id, target:{q,r}, source?:{q,r}, victims?:[{q,r}] }. */
export function abilityEffects(info, start, seed = 1) {
  const gen = new RNG(seed);
  const rnd = () => gen.next();
  const { id, target } = info;
  const fx = [];
  if (id === "volley") {
    const hexes = info.victims?.length ? info.victims : [target];
    for (const h of hexes) {
      for (let i = 0; i < 7; i++) {
        fx.push({ kind: "arrow", at: { q: h.q, r: h.r }, dx: (rnd() - 0.5) * 1.1, dy: (rnd() - 0.5) * 0.9, start: start + Math.floor(rnd() * 250), duration: ARROW_MS - 250 });
      }
    }
  } else if (id === "fireball") {
    fx.push({ kind: "burst", at: { q: target.q, r: target.r }, ring: 0, start, duration: BURST_MS });
    neighbors(target).forEach((n, i) => fx.push({ kind: "burst", at: n, ring: 1, start: start + 120 + i * 20, duration: BURST_MS - 150 }));
  } else if (id === "heal") {
    for (let i = 0; i < 6; i++) fx.push({ kind: "spark", at: { q: target.q, r: target.r }, dx: (rnd() - 0.5) * 0.9, dy: 0, start: start + i * 70, duration: PULSE_MS });
  } else if (id === "shieldwall" || id === "rally") {
    const hexes = [target, ...neighbors(target)];
    for (const h of hexes) fx.push({ kind: "pulse", style: id, at: { q: h.q, r: h.r }, start, duration: PULSE_MS });
  } else if (id === "envenom") {
    for (let i = 0; i < 4; i++) fx.push({ kind: "spark", poison: true, at: { q: target.q, r: target.r }, dx: (rnd() - 0.5) * 0.8, dy: 0, start: start + i * 90, duration: PULSE_MS });
  }
  return fx;
}

/** Progress 0..1 of an effect at `now`, or null when inactive. */
export function progress(fx, now) {
  const t = (now - fx.start) / fx.duration;
  return t < 0 || t > 1 ? null : t;
}

export function drawAbilityEffects(ctx, list, now, layout) {
  const s = layout.size;
  for (const fx of list) {
    const t = progress(fx, now);
    if (t === null) continue;
    const c = hexCenter(fx.at, layout);
    ctx.save();
    if (fx.kind === "arrow") {
      const x = c.x + fx.dx * s, y = c.y + fx.dy * s - (1 - t) * s * 2.4;
      ctx.globalAlpha = t > 0.9 ? 1 - (t - 0.9) * 10 : 1;
      ctx.strokeStyle = "#e8d9a8"; ctx.lineWidth = Math.max(1.5, s / 14);
      ctx.beginPath(); ctx.moveTo(x, y - s * 0.45); ctx.lineTo(x, y); ctx.stroke();
    } else if (fx.kind === "burst") {
      const r = s * (fx.ring ? 0.7 : 1.1) * (0.3 + 0.7 * t);
      ctx.globalAlpha = 1 - t;
      const g = ctx.createRadialGradient(c.x, c.y, 0, c.x, c.y, r);
      g.addColorStop(0, "#fff3b0"); g.addColorStop(0.5, "#ff9a3c"); g.addColorStop(1, "rgba(200,40,20,0)");
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(c.x, c.y, r, 0, Math.PI * 2); ctx.fill();
    } else if (fx.kind === "spark") {
      ctx.globalAlpha = 1 - t;
      ctx.fillStyle = fx.poison ? "#a56bd8" : "#7ddc6a";
      ctx.beginPath(); ctx.arc(c.x + fx.dx * s, c.y - t * s * 1.1, s * 0.12, 0, Math.PI * 2); ctx.fill();
    } else if (fx.kind === "pulse") {
      ctx.globalAlpha = (1 - t) * 0.8;
      ctx.strokeStyle = fx.style === "rally" ? "#ffd24a" : "#6aa9ff"; ctx.lineWidth = Math.max(2, s / 8);
      ctx.beginPath(); ctx.arc(c.x, c.y, s * (0.4 + 0.5 * t), 0, Math.PI * 2); ctx.stroke();
    }
    ctx.restore();
  }
}
