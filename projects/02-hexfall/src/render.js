// Canvas rendering of the hex map, overlays and simple terrain decorations.
import { toPixel, corners, fromPixel, key, SQRT3 } from "./hex.js";
import { terrain } from "./terrain.js";
import { fromOffset } from "./hex.js";
import { unitType, maxHp, maxMp } from "./units.js";

export const SIDE_COLORS = Object.freeze({ red: "#d0473f", blue: "#3f74d0" });

/** Layout: hex size and pixel origin so that the whole map fits `width`×`height`. */
export function fitLayout(map, width, height, margin = 12) {
  // pointy-top odd-r: width = sqrt3 * size * (cols + 0.5), height = size * (1.5 * rows + 0.5)
  const sizeW = (width - 2 * margin) / (SQRT3 * (map.cols + 0.5));
  const sizeH = (height - 2 * margin) / (1.5 * map.rows + 0.5);
  const size = Math.max(6, Math.min(sizeW, sizeH));
  const first = toPixel(fromOffset(0, 0), size);
  return { size, ox: margin + (SQRT3 * size) / 2 - first.x, oy: margin + size - first.y };
}

export function hexCenter(h, layout) {
  const p = toPixel(h, layout.size);
  return { x: p.x + layout.ox, y: p.y + layout.oy };
}

export function hexAtPixel(x, y, layout) {
  return fromPixel(x - layout.ox, y - layout.oy, layout.size);
}

function tracePath(ctx, pts) {
  ctx.beginPath();
  ctx.moveTo(pts[0].x, pts[0].y);
  for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i].x, pts[i].y);
  ctx.closePath();
}

/** Slight per-tile brightness variation so large fields don't look flat. */
export function shade(hexColor, amount) {
  const n = parseInt(hexColor.slice(1), 16);
  const f = (c) => Math.max(0, Math.min(255, Math.round(c + amount * 255)));
  const r = f(n >> 16), g = f((n >> 8) & 255), b = f(n & 255);
  return `#${((1 << 24) | (r << 16) | (g << 8) | b).toString(16).slice(1)}`;
}

function decorate(ctx, t, c, s) {
  ctx.save();
  switch (t.terrain) {
    case "forest": {
      ctx.fillStyle = "#2c5a2a";
      for (const [dx, dy] of [[-0.3, 0.1], [0.25, -0.05], [0, 0.35]]) {
        ctx.beginPath();
        ctx.moveTo(c.x + dx * s, c.y + (dy - 0.32) * s);
        ctx.lineTo(c.x + (dx - 0.2) * s, c.y + (dy + 0.08) * s);
        ctx.lineTo(c.x + (dx + 0.2) * s, c.y + (dy + 0.08) * s);
        ctx.fill();
      }
      break;
    }
    case "hills": {
      ctx.strokeStyle = "#7d6c43";
      ctx.lineWidth = Math.max(1, s / 12);
      for (const dx of [-0.25, 0.22]) {
        ctx.beginPath();
        ctx.arc(c.x + dx * s, c.y + 0.15 * s, 0.25 * s, Math.PI * 1.1, Math.PI * 1.9);
        ctx.stroke();
      }
      break;
    }
    case "mountain": {
      ctx.fillStyle = "#6c6762";
      ctx.beginPath();
      ctx.moveTo(c.x - 0.55 * s, c.y + 0.35 * s);
      ctx.lineTo(c.x - 0.05 * s, c.y - 0.5 * s);
      ctx.lineTo(c.x + 0.5 * s, c.y + 0.35 * s);
      ctx.fill();
      ctx.fillStyle = "#eeeeee";
      ctx.beginPath();
      ctx.moveTo(c.x - 0.18 * s, c.y - 0.28 * s);
      ctx.lineTo(c.x - 0.05 * s, c.y - 0.5 * s);
      ctx.lineTo(c.x + 0.09 * s, c.y - 0.27 * s);
      ctx.fill();
      break;
    }
    case "village": {
      ctx.fillStyle = t.owner ? SIDE_COLORS[t.owner] : "#7a4a24";
      ctx.fillRect(c.x - 0.3 * s, c.y - 0.05 * s, 0.6 * s, 0.38 * s);
      ctx.beginPath();
      ctx.moveTo(c.x - 0.4 * s, c.y - 0.05 * s);
      ctx.lineTo(c.x, c.y - 0.42 * s);
      ctx.lineTo(c.x + 0.4 * s, c.y - 0.05 * s);
      ctx.fill();
      break;
    }
    case "swamp": {
      ctx.strokeStyle = "#3e5636";
      ctx.lineWidth = Math.max(1, s / 14);
      for (const dy of [-0.15, 0.2]) {
        ctx.beginPath();
        ctx.moveTo(c.x - 0.35 * s, c.y + dy * s);
        ctx.lineTo(c.x + 0.35 * s, c.y + dy * s);
        ctx.stroke();
      }
      break;
    }
    case "bridge": {
      ctx.fillStyle = "#3d78b0";
      ctx.fillRect(c.x - 0.6 * s, c.y - 0.42 * s, 1.2 * s, 0.2 * s);
      ctx.fillRect(c.x - 0.6 * s, c.y + 0.22 * s, 1.2 * s, 0.2 * s);
      ctx.strokeStyle = "#6e5434";
      ctx.lineWidth = Math.max(1, s / 14);
      for (const dx of [-0.3, 0, 0.3]) {
        ctx.beginPath();
        ctx.moveTo(c.x + dx * s, c.y - 0.2 * s);
        ctx.lineTo(c.x + dx * s, c.y + 0.2 * s);
        ctx.stroke();
      }
      break;
    }
    case "river":
    case "water":
    case "shallows": {
      ctx.strokeStyle = "rgba(255,255,255,0.25)";
      ctx.lineWidth = Math.max(1, s / 16);
      ctx.beginPath();
      ctx.arc(c.x - 0.15 * s, c.y, 0.18 * s, Math.PI * 1.15, Math.PI * 1.85);
      ctx.arc(c.x + 0.2 * s, c.y + 0.1 * s, 0.18 * s, Math.PI * 1.15, Math.PI * 1.85);
      ctx.stroke();
      break;
    }
    default:
      break;
  }
  ctx.restore();
}

/**
 * Draw the whole battlefield.
 * @param {CanvasRenderingContext2D} ctx
 * @param {import("./map.js").HexMap} map
 * @param {object} layout from fitLayout
 * @param {object} [overlay] {reach: Map, path: Hex[], hover: Hex, spawns: Hex[][], selected: Hex}
 */
export function drawMap(ctx, map, layout, overlay = {}) {
  const s = layout.size;
  ctx.fillStyle = "#1b1f24";
  ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  for (const t of map) {
    const c = hexCenter(t, layout);
    const pts = corners(c.x, c.y, s - 0.5);
    const base = terrain(t.terrain).color;
    tracePath(ctx, pts);
    ctx.fillStyle = shade(base, (t.elevation - 0.5) * 0.18);
    ctx.fill();
    if (t.terrain === "road") {
      ctx.fillStyle = "#9c8660";
      ctx.beginPath();
      ctx.arc(c.x, c.y, s * 0.18, 0, Math.PI * 2);
      ctx.fill();
    }
    decorate(ctx, t, c, s);
  }
  const zoneColors = [SIDE_COLORS.red, SIDE_COLORS.blue];
  (overlay.spawns ?? []).forEach((zone, i) => {
    for (const h of zone) outline(ctx, hexCenter(h, layout), s, zoneColors[i], 2, [4, 3]);
  });
  if (overlay.reach) {
    ctx.fillStyle = "rgba(255, 236, 110, 0.4)";
    for (const node of overlay.reach.values()) {
      const c = hexCenter(node.hex, layout);
      tracePath(ctx, corners(c.x, c.y, s - 1));
      ctx.fill();
    }
  }
  if (overlay.path && overlay.path.length > 1) {
    ctx.strokeStyle = "#fff3a0";
    ctx.lineWidth = Math.max(2, s / 6);
    ctx.lineCap = "round";
    ctx.beginPath();
    overlay.path.forEach((h, i) => {
      const c = hexCenter(h, layout);
      if (i === 0) ctx.moveTo(c.x, c.y);
      else ctx.lineTo(c.x, c.y);
    });
    ctx.stroke();
  }
  if (overlay.targets) {
    for (const h of overlay.targets) outline(ctx, hexCenter(h, layout), s, "#ff5a4a", 3);
  }
  if (overlay.attackFrom) outline(ctx, hexCenter(overlay.attackFrom, layout), s, "#ffb04a", 2, [3, 3]);
  if (overlay.selected) outline(ctx, hexCenter(overlay.selected, layout), s, "#ffffff", 3);
  if (overlay.hover && map.has(overlay.hover)) outline(ctx, hexCenter(overlay.hover, layout), s, "rgba(255,255,255,0.7)", 2);
}

function outline(ctx, c, s, color, width, dash = []) {
  ctx.save();
  ctx.setLineDash(dash);
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  tracePath(ctx, corners(c.x, c.y, s - 2));
  ctx.stroke();
  ctx.restore();
}

/**
 * Draw unit tokens: a disc in the side colour with the type letter, an HP bar of pips
 * (one pip per 10% of max HP), veteran stars, and a dimmed look once a unit is spent.
 * @param {object} [opts] {selected: unit id, positions: Map<id, {x, y}> for animated units,
 *                        activeSide: side id (its spent units are dimmed)}
 */
export function drawUnits(ctx, units, layout, opts = {}) {
  const s = layout.size;
  const r = s * 0.55;
  for (const u of units) {
    if (u.hp <= 0) continue;
    const c = opts.positions?.get(u.id) ?? hexCenter(u, layout);
    const exhausted = opts.activeSide === u.side && (u.acted || u.mp <= 0);
    ctx.save();
    ctx.globalAlpha = exhausted ? 0.62 : 1;
    ctx.fillStyle = "rgba(0,0,0,0.35)";
    ctx.beginPath();
    ctx.ellipse(c.x, c.y + r * 0.85, r * 0.9, r * 0.32, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = SIDE_COLORS[u.side] ?? "#888";
    ctx.strokeStyle = opts.selected === u.id ? "#ffffff" : "#15181c";
    ctx.lineWidth = opts.selected === u.id ? Math.max(2, s / 8) : Math.max(1, s / 14);
    ctx.beginPath();
    ctx.arc(c.x, c.y, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "#ffffff";
    ctx.font = `bold ${Math.round(r * 1.05)}px system-ui, sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(unitType(u).glyph, c.x, c.y + 1);
    // HP pips
    const pips = 10, filled = Math.ceil((u.hp / maxHp(u)) * pips);
    const pw = (r * 2) / pips;
    for (let i = 0; i < pips; i++) {
      ctx.fillStyle = i < filled ? (filled <= 3 ? "#ff5a4a" : filled <= 6 ? "#f0c05a" : "#7ddc6a") : "#2a2f36";
      ctx.fillRect(c.x - r + i * pw + 0.5, c.y - r - s * 0.22, pw - 1, Math.max(2, s * 0.12));
    }
    // veteran stars
    for (let i = 1; i < (u.level ?? 1); i++) {
      ctx.fillStyle = "#ffd75a";
      ctx.font = `${Math.round(r * 0.7)}px system-ui, sans-serif`;
      ctx.fillText("★", c.x - r * 0.9 + (i - 1) * r * 0.6, c.y + r * 0.9);
    }
    // move points left (small dot, active side only)
    if (opts.activeSide === u.side && u.mp > 0 && u.mp < maxMp(u)) {
      ctx.fillStyle = "#f0c05a";
      ctx.beginPath();
      ctx.arc(c.x + r * 0.85, c.y + r * 0.75, Math.max(2, r * 0.18), 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }
}

export { key };
