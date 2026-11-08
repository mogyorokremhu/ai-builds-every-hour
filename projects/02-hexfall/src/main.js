// Browser entry point (Phase 1 map viewer): generate maps, inspect terrain, preview movement,
// zoom (mouse wheel) and pan (drag) with a minimap.
import { generate, terrainCounts } from "./mapgen.js";
import { drawMap, fitLayout, hexAtPixel } from "./render.js";
import { reachable, pathTo } from "./pathfind.js";
import { terrain, TERRAIN } from "./terrain.js";
import { seedFrom } from "./rng.js";
import { key } from "./hex.js";
import { camera, view, zoomAt, panBy, visibleRect, centerOn, clamp } from "./camera.js";

const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");
const mini = document.getElementById("minimap");
const mctx = mini.getContext("2d");
const info = document.getElementById("info");
const seedInput = document.getElementById("seed");
const mpInput = document.getElementById("mp");
const symInput = document.getElementById("sym");

const state = { gen: null, cam: null, viewport: { width: 0, height: 0 }, selected: null, hover: null, reach: null };
const drag = { active: false, moved: false, x: 0, y: 0 };

function parseSeed(text) {
  const t = text.trim();
  return /^\d+$/.test(t) ? Number(t) : seedFrom(t || "hexfall");
}

function newMap(seedText) {
  state.gen = generate({ seed: parseSeed(seedText), symmetric: symInput.checked });
  state.selected = state.reach = null;
  state.cam = null;
  resize();
  const counts = terrainCounts(state.gen.map);
  document.getElementById("legend").innerHTML = Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .map(([id, n]) => `<span class="sw" style="background:${TERRAIN[id].color}"></span>${TERRAIN[id].name} ${n}`)
    .join(" · ");
  location.hash = encodeURIComponent(seedText);
}

function sizeCanvas(cv, c, w, h) {
  const dpr = window.devicePixelRatio || 1;
  cv.style.width = `${w}px`;
  cv.style.height = `${h}px`;
  cv.width = Math.round(w * dpr);
  cv.height = Math.round(h * dpr);
  c.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function resize() {
  const box = canvas.parentElement.getBoundingClientRect();
  const m = state.gen.map;
  const aspect = (1.5 * m.rows + 0.5) / (Math.sqrt(3) * (m.cols + 0.5));
  const w = Math.max(320, box.width);
  const h = Math.max(240, Math.min(window.innerHeight - 160, w * aspect + 24));
  sizeCanvas(canvas, ctx, w, h);
  state.viewport = { width: w, height: h };
  const base = fitLayout(m, w, h);
  state.cam = state.cam ? clamp({ ...state.cam, base }, state.viewport) : camera(base);
  const mw = 180, mh = Math.round(180 * (h / w));
  sizeCanvas(mini, mctx, mw, mh);
  state.miniLayout = fitLayout(m, mw, mh, 4);
  draw();
}

function draw() {
  const { map, spawns } = state.gen;
  const path = state.reach && state.hover ? pathTo(state.reach, state.hover) : null;
  drawMap(ctx, map, view(state.cam), { spawns, reach: state.reach, path, hover: state.hover, selected: state.selected });
  drawMinimap();
}

function drawMinimap() {
  drawMap(mctx, state.gen.map, state.miniLayout, { spawns: state.gen.spawns });
  if (state.cam.zoom <= 1) return;
  const r = visibleRect(state.cam, state.viewport);
  const sx = mini.clientWidth / state.viewport.width, sy = mini.clientHeight / state.viewport.height;
  mctx.strokeStyle = "#ffffff";
  mctx.lineWidth = 1.5;
  mctx.strokeRect(r.x * sx, r.y * sy, r.w * sx, r.h * sy);
}

function describe(h) {
  const t = state.gen.map.get(h);
  if (!t) return "";
  const tr = terrain(t.terrain);
  const cost = Number.isFinite(tr.cost) ? `move ${tr.cost}` : "impassable";
  const extra = state.reach?.has(key(h)) ? ` — reachable for ${state.reach.get(key(h)).cost} MP` : "";
  return `(${h.q}, ${h.r}) ${tr.name}: ${cost}, defence ${tr.defense}%${tr.blocksSight ? ", blocks sight" : ""}${extra}`;
}

function local(ev, el = canvas) {
  const r = el.getBoundingClientRect();
  return { x: ev.clientX - r.left, y: ev.clientY - r.top };
}

function select(h) {
  const map = state.gen.map;
  if (!map.has(h) || !map.passable(h)) {
    state.selected = state.reach = null;
  } else {
    state.selected = h;
    state.reach = reachable(map, h, Number(mpInput.value) || 4);
  }
  info.textContent = state.selected ? describe(state.selected) : "";
  draw();
}

canvas.addEventListener("mousedown", (ev) => {
  Object.assign(drag, { active: true, moved: false, x: ev.clientX, y: ev.clientY });
});
window.addEventListener("mouseup", (ev) => {
  if (drag.active && !drag.moved && ev.target === canvas) {
    const p = local(ev);
    select(hexAtPixel(p.x, p.y, view(state.cam)));
  }
  drag.active = false;
});
canvas.addEventListener("mousemove", (ev) => {
  if (drag.active) {
    const dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
    if (drag.moved || Math.hypot(dx, dy) > 4) {
      drag.moved = true;
      state.cam = panBy(state.cam, dx, dy, state.viewport);
      drag.x = ev.clientX;
      drag.y = ev.clientY;
      draw();
      return;
    }
  }
  const p = local(ev);
  const h = hexAtPixel(p.x, p.y, view(state.cam));
  if (state.hover && key(state.hover) === key(h)) return;
  state.hover = state.gen.map.has(h) ? h : null;
  info.textContent = state.hover ? describe(state.hover) : "Click a hex to preview movement from it.";
  draw();
});
canvas.addEventListener("wheel", (ev) => {
  ev.preventDefault();
  const p = local(ev);
  state.cam = zoomAt(state.cam, ev.deltaY < 0 ? 1.15 : 1 / 1.15, p.x, p.y, state.viewport);
  draw();
}, { passive: false });
mini.addEventListener("click", (ev) => {
  const p = local(ev, mini);
  const bx = (p.x / mini.clientWidth) * state.viewport.width;
  const by = (p.y / mini.clientHeight) * state.viewport.height;
  state.cam = centerOn(state.cam, bx, by, state.viewport);
  draw();
});

document.getElementById("generate").addEventListener("click", () => newMap(seedInput.value));
document.getElementById("random").addEventListener("click", () => {
  seedInput.value = String(Math.floor(Math.random() * 1e6));
  newMap(seedInput.value);
});
document.getElementById("zoomreset").addEventListener("click", () => {
  state.cam = camera(state.cam.base);
  draw();
});
mpInput.addEventListener("change", () => {
  if (state.selected) state.reach = reachable(state.gen.map, state.selected, Number(mpInput.value) || 4);
  draw();
});
symInput.addEventListener("change", () => newMap(seedInput.value));
window.addEventListener("resize", resize);

seedInput.value = decodeURIComponent(location.hash.slice(1)) || "1";
newMap(seedInput.value);
