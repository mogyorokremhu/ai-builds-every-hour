// Canvas rendering of the hex map, overlays and simple terrain decorations.
import { toPixel, corners, fromPixel, key, SQRT3 } from "./hex.js";
import { terrain } from "./terrain.js";
import { fromOffset } from "./hex.js";
import { unitType, maxHp, maxMp } from "./units.js";
import { activeStatuses, STATUS } from "./status.js";

export const SIDE_COLORS = { red: "#d0473f", blue: "#3f74d0" }; // mutable so themes can recolour (palette.js applyTheme)

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
      if (t.owner) drawFlag(ctx, c, s, SIDE_COLORS[t.owner] ?? "#888");
      break;
    }
    case "keep":
    case "castle": {
      // crenellated wall ring; the keep gets a tower
      ctx.strokeStyle = "#5d564d";
      ctx.lineWidth = Math.max(1, s / 10);
      ctx.beginPath();
      ctx.arc(c.x, c.y, s * 0.55, 0, Math.PI * 2);
      ctx.stroke();
      ctx.fillStyle = "#5d564d";
      for (let i = 0; i < 6; i++) {
        const a = (Math.PI / 3) * i + Math.PI / 6;
        ctx.fillRect(c.x + Math.cos(a) * s * 0.55 - s * 0.07, c.y + Math.sin(a) * s * 0.55 - s * 0.07, s * 0.14, s * 0.14);
      }
      if (t.terrain === "keep") {
        ctx.fillStyle = "#4a443d";
        ctx.fillRect(c.x - s * 0.18, c.y - s * 0.32, s * 0.36, s * 0.5);
        ctx.fillRect(c.x - s * 0.24, c.y - s * 0.4, s * 0.12, s * 0.1);
        ctx.fillRect(c.x + s * 0.12, c.y - s * 0.4, s * 0.12, s * 0.1);
      }
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
    case "ruins": {
      // broken wall stubs and a fallen arch
      ctx.fillStyle = "#6a6358";
      for (const [dx, dy, h] of [[-0.38, 0.05, 0.32], [-0.12, -0.08, 0.45], [0.18, 0.02, 0.25], [0.36, -0.04, 0.38]]) {
        ctx.fillRect(c.x + dx * s, c.y + (dy - h + 0.25) * s, 0.14 * s, h * s);
      }
      ctx.strokeStyle = "#5a544a";
      ctx.lineWidth = Math.max(1, s / 12);
      ctx.beginPath();
      ctx.arc(c.x - 0.05 * s, c.y + 0.05 * s, 0.2 * s, Math.PI * 1.05, Math.PI * 1.6);
      ctx.stroke();
      ctx.fillStyle = "#7d7568";
      ctx.fillRect(c.x - 0.45 * s, c.y + 0.3 * s, 0.9 * s, 0.07 * s);
      break;
    }
    case "ford": {
      // stepping stones across the water
      ctx.fillStyle = "#c9c0a8";
      for (const [dx, dy] of [[-0.4, 0.15], [-0.15, -0.05], [0.12, 0.12], [0.38, -0.08]]) {
        ctx.beginPath();
        ctx.ellipse(c.x + dx * s, c.y + dy * s, 0.12 * s, 0.08 * s, 0, 0, Math.PI * 2);
        ctx.fill();
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

/** A little side-coloured flag on a pole (village ownership). */
export function drawFlag(ctx, c, s, color) {
  const x = c.x + 0.42 * s, top = c.y - 0.62 * s;
  ctx.strokeStyle = "#2a2118";
  ctx.lineWidth = Math.max(1, s / 16);
  ctx.beginPath();
  ctx.moveTo(x, top);
  ctx.lineTo(x, c.y + 0.1 * s);
  ctx.stroke();
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(x, top);
  ctx.lineTo(x + 0.34 * s, top + 0.11 * s);
  ctx.lineTo(x, top + 0.22 * s);
  ctx.closePath();
  ctx.fill();
  ctx.strokeStyle = "rgba(255,255,255,0.8)";
  ctx.lineWidth = Math.max(0.5, s / 30);
  ctx.stroke();
}

/**
 * Draw the whole battlefield.
 * @param {CanvasRenderingContext2D} ctx
 * @param {import("./map.js").HexMap} map
 * @param {object} layout from fitLayout
 * @param {object} [overlay] {reach: Map, path: Hex[], hover: Hex, spawns: Hex[][], selected: Hex,
 *   tint: css colour laid over the terrain (time of day), weatherTint: css colour (rain, fog...),
 *   recruit: Hex[] free recruit hexes, abilityTargets: Hex[], blast: Hex[] (fireball preview),
 *   visible: Set<key>|null and explored: Set<key>|null (fog of war for the viewing side)}
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
    if (t.fire > 0) drawFire(ctx, c, s, t.fire);
  }
  for (const tint of [overlay.tint, overlay.weatherTint]) {
    if (!tint) continue;
    ctx.fillStyle = tint;
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  }
  if (overlay.visible) {
    // fog of war: explored-but-unseen hexes are dimmed, never-seen ones nearly black
    for (const t of map) {
      const k = key(t);
      if (overlay.visible.has(k)) continue;
      const c = hexCenter(t, layout);
      tracePath(ctx, corners(c.x, c.y, s));
      ctx.fillStyle = overlay.explored?.has(k) ? "rgba(10,12,16,0.5)" : "rgba(8,9,12,0.92)";
      ctx.fill();
    }
  }
  for (const h of overlay.recruit ?? []) outline(ctx, hexCenter(h, layout), s, "#7ddc6a", 2, [2, 3]);
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
  for (const h of overlay.abilityTargets ?? []) outline(ctx, hexCenter(h, layout), s, "#c78bff", 3, [5, 3]);
  if (overlay.blast?.length) {
    ctx.fillStyle = "rgba(255,120,40,0.35)";
    for (const h of overlay.blast) {
      if (!map.has(h)) continue;
      const c = hexCenter(h, layout);
      tracePath(ctx, corners(c.x, c.y, s - 1));
      ctx.fill();
    }
  }
  if (overlay.attackFrom) outline(ctx, hexCenter(overlay.attackFrom, layout), s, "#ffb04a", 2, [3, 3]);
  if (overlay.selected) outline(ctx, hexCenter(overlay.selected, layout), s, "#ffffff", 3);
  if (overlay.hover && map.has(overlay.hover)) outline(ctx, hexCenter(overlay.hover, layout), s, "rgba(255,255,255,0.7)", 2);
}

/** Flames on a burning hex (taller while it has more turns left). */
export function drawFire(ctx, c, s, turns) {
  ctx.save();
  const h = 0.25 + Math.min(3, turns) * 0.08;
  for (const [dx, k] of [[-0.25, 0.8], [0, 1.1], [0.25, 0.9]]) {
    const x = c.x + dx * s, base = c.y + 0.3 * s, top = base - h * k * s;
    ctx.fillStyle = "rgba(255,110,30,0.9)";
    ctx.beginPath();
    ctx.moveTo(x - 0.12 * s, base);
    ctx.quadraticCurveTo(x - 0.1 * s, top + 0.1 * s, x, top);
    ctx.quadraticCurveTo(x + 0.1 * s, top + 0.1 * s, x + 0.12 * s, base);
    ctx.fill();
    ctx.fillStyle = "rgba(255,220,90,0.9)";
    ctx.beginPath();
    ctx.ellipse(x, base - 0.07 * s, 0.05 * s, 0.1 * s * k, 0, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();
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
 * Status effects are drawn as small icons above the token.
 * @param {object} [opts] {selected: unit id, positions: Map<id, {x, y}> for animated units,
 *                        activeSide: side id (its spent units are dimmed),
 *                        isVisible: (unit) => boolean (fog of war: hidden units are skipped)}
 */
export function drawUnits(ctx, units, layout, opts = {}) {
  const s = layout.size;
  const r = s * 0.55;
  for (const u of units) {
    if (u.hp <= 0) continue;
    if (opts.isVisible && !opts.isVisible(u)) continue;
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
    // status icons above the HP bar
    const st = activeStatuses(u);
    if (st.length && s >= 12) {
      ctx.font = `${Math.round(r * 0.62)}px system-ui, sans-serif`;
      st.forEach((id, i) => ctx.fillText(STATUS[id].icon, c.x - ((st.length - 1) * r * 0.36) + i * r * 0.72, c.y - r - s * 0.48));
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
