// Browser entry point: a battle on a generated map against the AI or hot-seat — select, move,
// attack, recruit, end turn — plus zoom/pan, minimap, roster, economy panel, day/night strip,
// combat log, damage previews, undo and saves.
import { Game, SIDES } from "./game.js";
import { drawMap, drawUnits, fitLayout, hexAtPixel, hexCenter } from "./render.js";
import { routeTo } from "./movement.js";
import { terrain, TERRAIN } from "./terrain.js";
import { terrainCounts } from "./mapgen.js";
import { seedFrom } from "./rng.js";
import { key } from "./hex.js";
import { camera, view, zoomAt, panBy, visibleRect, centerOn, clamp } from "./camera.js";
import { describeUnit, unitType, maxHp, maxMp, RECRUITABLE, UNIT_TYPES } from "./units.js";
import { AIPlayer, DIFFICULTY } from "./ai.js";
import { ownedVillages, income } from "./economy.js";
import { upcoming } from "./timeofday.js";
import { moveAnimation, lungeAnimation, animatedPosition, finished } from "./animate.js";
import { serialize, deserialize, saveToSlot, loadFromSlot } from "./save.js";

const $ = (id) => document.getElementById(id);
const canvas = $("board");
const ctx = canvas.getContext("2d");
const mini = $("minimap");
const mctx = mini.getContext("2d");
const info = $("info");
const tip = $("tip");
const seedInput = $("seed");
const symInput = $("sym");

const state = {
  game: null, cam: null, viewport: { width: 0, height: 0 }, miniLayout: null,
  selected: null, area: null, hover: null, anims: [], busy: false,
  ai: { red: null, blue: null }, // AIPlayer per side, null = human
};
const AI_PREF = "hexfall.ai";
const drag = { active: false, moved: false, x: 0, y: 0 };

function storage() {
  try {
    return window.localStorage;
  } catch {
    return null;
  }
}

function parseSeed(text) {
  const t = text.trim();
  return /^\d+$/.test(t) ? Number(t) : seedFrom(t || "hexfall");
}

function newBattle(seedText) {
  setGame(Game.create({ seed: parseSeed(seedText), symmetric: symInput.checked }));
  location.hash = encodeURIComponent(seedText);
}

function setGame(game) {
  state.game = game;
  setupAi();
  state.selected = state.area = null;
  state.cam = null;
  state.anims = [];
  resize();
  const counts = terrainCounts(game.map);
  $("legend").innerHTML = Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .map(([id, n]) => `<span class="sw" style="background:${TERRAIN[id].color}"></span>${TERRAIN[id].name} ${n}`)
    .join(" · ");
  refresh();
  runAi();
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
  const m = state.game.map;
  const aspect = (1.5 * m.rows + 0.5) / (Math.sqrt(3) * (m.cols + 0.5));
  const w = Math.max(300, box.width);
  const h = Math.max(220, Math.min(window.innerHeight - 170, w * aspect + 24));
  sizeCanvas(canvas, ctx, w, h);
  state.viewport = { width: w, height: h };
  const base = fitLayout(m, w, h);
  state.cam = state.cam ? clamp({ ...state.cam, base }, state.viewport) : camera(base);
  const mw = Math.min(180, w * 0.3), mh = Math.round(mw * (h / w));
  sizeCanvas(mini, mctx, mw, mh);
  state.miniLayout = fitLayout(m, mw, mh, 4);
  draw();
}

// ---------------------------------------------------------------- drawing

function selectedUnit() {
  return state.selected == null ? null : state.game.unitById(state.selected);
}

function draw(now = performance.now()) {
  const g = state.game;
  const layout = view(state.cam);
  const sel = selectedUnit();
  const overlay = {
    spawns: g.turn === 1 && g.active === 0 ? g.spawns : [], hover: state.hover, tint: g.timeOfDay().tint,
    recruit: state.recruitMode && !isAiTurn() ? g.recruitHexes() : [],
  };
  if (sel && state.area && !state.busy) {
    overlay.reach = new Map([...state.area].filter(([, n]) => n.canStop));
    overlay.selected = sel;
    overlay.targets = g.units.filter((t) => t.side !== sel.side && g.attackPlan(sel, t));
    const hoverUnit = state.hover && g.unitAt(state.hover);
    if (hoverUnit && hoverUnit.side !== sel.side) {
      const plan = g.attackPlan(sel, hoverUnit);
      if (plan && key(plan.from) !== key(sel)) overlay.attackFrom = plan.from;
    } else if (state.hover) {
      overlay.path = routeTo(state.area, state.hover);
    }
  }
  drawMap(ctx, g.map, layout, overlay);
  const positions = new Map();
  for (const a of state.anims) positions.set(a.unitId, animatedPosition(a, now, layout));
  drawUnits(ctx, g.units, layout, { selected: state.selected, positions, activeSide: g.side });
  drawMinimap();
}

function drawMinimap() {
  const g = state.game;
  drawMap(mctx, g.map, state.miniLayout, {});
  drawUnits(mctx, g.units, state.miniLayout, {});
  if (state.cam.zoom <= 1) return;
  const r = visibleRect(state.cam, state.viewport);
  const sx = mini.clientWidth / state.viewport.width, sy = mini.clientHeight / state.viewport.height;
  mctx.strokeStyle = "#ffffff";
  mctx.lineWidth = 1.5;
  mctx.strokeRect(r.x * sx, r.y * sy, r.w * sx, r.h * sy);
}

function animate(anims) {
  return new Promise((resolve) => {
    state.anims = anims;
    state.busy = true;
    const frame = (now) => {
      draw(now);
      if (state.anims.every((a) => finished(a, now))) {
        state.anims = [];
        state.busy = false;
        draw();
        resolve();
      } else {
        requestAnimationFrame(frame);
      }
    };
    requestAnimationFrame(frame);
  });
}

// ---------------------------------------------------------------- panels

function sideName(id) {
  return SIDES.find((s) => s.id === id)?.name ?? id;
}

function refresh() {
  const g = state.game;
  const turnEl = $("turn");
  const tod = g.timeOfDay();
  turnEl.textContent = g.winner === "draw" ? "Draw!" : g.winner ? `${sideName(g.winner)} wins!`
    : `Turn ${g.turn}${g.rules.turnLimit ? `/${g.rules.turnLimit}` : ""} · ${tod.icon} ${tod.name} — ${sideName(g.side)}${isAiTurn() ? " (AI)" : ""} to move`;
  turnEl.className = `turn ${g.winner ?? g.side}`;
  $("undo").disabled = !g.canUndo() || state.busy || isAiTurn();
  $("endturn").disabled = !!g.winner || state.busy || isAiTurn();
  renderEconomy();
  renderRecruit();
  renderDayNight();
  renderRoster();
  renderLog();
  renderUnitInfo();
  draw();
}

function renderRoster() {
  const g = state.game;
  const ul = $("roster");
  ul.innerHTML = "";
  for (const side of SIDES) {
    const head = document.createElement("li");
    head.className = `rhead ${side.id}`;
    const n = g.unitsOf(side.id).length;
    const v = ownedVillages(g, side.id).length;
    head.textContent = `${side.name}${state.ai[side.id] ? " (AI)" : ""} — ${n} unit${n === 1 ? "" : "s"} · ⚑ ${v}`;
    ul.append(head);
    for (const u of g.unitsOf(side.id)) {
      const li = document.createElement("li");
      li.className = `runit ${side.id}${u.id === state.selected ? " sel" : ""}${side.id === g.side && (u.acted || u.mp <= 0) ? " spent" : ""}`;
      li.tabIndex = 0;
      const pct = Math.round((u.hp / maxHp(u)) * 100);
      li.innerHTML = `<b>${unitType(u).glyph}</b> ${unitType(u).name}${"★".repeat(u.level - 1)}
        <span class="hp"><i style="width:${pct}%"></i></span><small>${u.hp}/${maxHp(u)} · ${u.mp}/${maxMp(u)} MP</small>`;
      li.addEventListener("click", () => focusUnit(u));
      li.addEventListener("keydown", (ev) => { if (ev.key === "Enter") focusUnit(u); });
      ul.append(li);
    }
  }
}

function renderEconomy() {
  const g = state.game;
  const target = g.holdTarget();
  $("economy").innerHTML = SIDES.map((side, i) => {
    const v = ownedVillages(g, side.id).length;
    const hold = target && g.hold[i] ? ` · holding ${g.hold[i]}/${g.rules.holdTurns}` : "";
    return `<div class="eco ${side.id}${g.side === side.id ? " now" : ""}"><b>${side.name}</b>
      <span title="gold">🪙 ${g.gold[i]}</span> <span title="income per turn">+${income(g, side.id)}</span>
      <span title="villages">⚑ ${v}/${g.villages.length}</span>${hold}</div>`;
  }).join("") + (target ? `<p class="goal">Win: rout the enemy, hold ${target} villages for ${g.rules.holdTurns} turns,
    or lead on points after turn ${g.rules.turnLimit}.</p>` : "");
}

function renderRecruit() {
  const g = state.game;
  const el = $("recruit");
  el.innerHTML = "";
  const human = !isAiTurn() && !g.winner;
  for (const type of RECRUITABLE) {
    const t = UNIT_TYPES[type];
    const b = document.createElement("button");
    const problem = human ? g.recruitProblem(type) : "not your turn";
    b.className = "rbtn";
    b.disabled = !!problem || state.busy;
    b.title = `${t.name} (${t.alignment}) — ${t.blurb}${problem ? ` [${problem}]` : ""}`;
    b.innerHTML = `<b>${t.glyph}</b> ${t.name} <small>${t.cost}g</small>`;
    b.addEventListener("click", () => doRecruit(type));
    b.addEventListener("mouseenter", () => { state.recruitMode = true; draw(); });
    b.addEventListener("mouseleave", () => { state.recruitMode = false; draw(); });
    el.append(b);
  }
}

function renderDayNight() {
  const g = state.game;
  $("daynight").innerHTML = upcoming(g.turn, 6).map((p, i) =>
    `<span class="tod${i === 0 ? " now" : ""}" title="Turn ${p.turn}: ${p.name} — lawful ${p.lawful >= 0 ? "+" : ""}${p.lawful}%, chaotic ${p.lawful <= 0 ? "+" : ""}${-p.lawful}%">${p.icon}</span>`).join("");
}

function renderLog() {
  const el = $("log");
  el.innerHTML = state.game.log.slice(-40).map((l) => `<li class="${l.side}">${escapeHtml(l.text)}</li>`).join("");
  el.scrollTop = el.scrollHeight;
}

function renderUnitInfo() {
  const u = selectedUnit();
  $("unitinfo").textContent = u ? `${sideName(u.side)} ${describeUnit(u)} — ${unitType(u).blurb}` : "";
}

function escapeHtml(s) {
  return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
}

function focusUnit(u) {
  const g = state.game;
  if (u.side === g.side && !g.winner) select(u);
  else {
    state.selected = u.id;
    state.area = null;
  }
  if (state.cam.zoom > 1) {
    const c = hexCenter(u, state.cam.base);
    state.cam = centerOn(state.cam, c.x, c.y, state.viewport);
  }
  refresh();
}

// ---------------------------------------------------------------- AI

function readAiPref() {
  try {
    return JSON.parse(storage()?.getItem(AI_PREF) ?? "null") ?? { red: "human", blue: "normal" };
  } catch {
    return { red: "human", blue: "normal" };
  }
}

function setupAi() {
  const pref = { red: $("redai").value, blue: $("blueai").value };
  for (const side of SIDES) {
    const d = pref[side.id];
    state.ai[side.id] = DIFFICULTY[d] ? new AIPlayer(side.id, { difficulty: d, seed: state.game.seed + (side.id === "red" ? 11 : 23) }) : null;
  }
  try {
    storage()?.setItem(AI_PREF, JSON.stringify(pref));
  } catch {
    // preferences are optional
  }
}

function isAiTurn() {
  const g = state.game;
  return !!g && !g.winner && !!state.ai[g.side];
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** Let the AI play the active side's turn with animations, then hand back control. */
async function runAi() {
  const g = state.game;
  if (state.aiRunning || !isAiTurn()) return;
  state.aiRunning = true;
  const game = g;
  try {
    for (let guard = 0; guard < 300 && state.game === game && isAiTurn(); guard++) {
      const player = state.ai[g.side];
      const a = player.nextAction(g);
      if (a.type === "end") {
        g.endTurn();
        select(null);
        autosave();
        refresh();
        if (!isAiTurn()) break;
        await sleep(250);
        continue;
      }
      const u = a.unitId != null ? g.unitById(a.unitId) : null;
      if (a.type === "move") {
        const route = routeTo(g.area(u), a.to);
        if (route) await animate([moveAnimation(u.id, route, performance.now())]);
      } else if (a.type === "attack") {
        const t = g.unitById(a.targetId);
        if (key(a.from) !== key(u)) {
          const route = routeTo(g.area(u), a.from);
          if (route) await animate([moveAnimation(u.id, route, performance.now())]);
        }
        await animate([lungeAnimation(u.id, a.from, t, performance.now())]);
      }
      if (state.game !== game) break;
      player.play(g, a);
      refresh();
      if (a.type !== "hold") await sleep(a.type === "recruit" ? 200 : 120);
    }
  } finally {
    state.aiRunning = false;
    autosave();
    refresh();
  }
}

// ---------------------------------------------------------------- actions

function doRecruit(type) {
  const g = state.game;
  if (state.busy || isAiTurn() || g.recruitProblem(type)) return;
  const u = g.recruit(type);
  select(null);
  state.selected = u.id;
  autosave();
  refresh();
}

function select(u) {
  state.selected = u ? u.id : null;
  state.area = u && u.side === state.game.side ? state.game.area(u) : null;
}

function autosave() {
  const s = storage();
  if (!s) return;
  try {
    saveToSlot(s, "auto", state.game);
  } catch {
    // storage full or blocked: saving is a convenience
  }
}

async function doMove(u, dest) {
  const g = state.game;
  const route = g.move(u, dest);
  await animate([moveAnimation(u.id, route, performance.now())]);
  select(u.mp > 0 || g.targets(u).length ? u : null);
  autosave();
  refresh();
}

async function doAttack(u, target) {
  const g = state.game;
  const plan = g.attackPlan(u, target);
  if (!plan) return;
  const start = { q: u.q, r: u.r };
  if (key(plan.from) !== key(start)) {
    const route = routeTo(g.area(u), plan.from);
    if (route) await animate([moveAnimation(u.id, route, performance.now())]);
  }
  await animate([lungeAnimation(u.id, plan.from, target, performance.now())]);
  g.attack(u, target);
  select(null);
  autosave();
  refresh();
}

function onClick(h) {
  const g = state.game;
  if (state.busy || isAiTurn()) return;
  hideTip();
  const clicked = g.unitAt(h);
  const sel = selectedUnit();
  if (sel && sel.side === g.side && clicked && clicked.side !== sel.side && g.attackPlan(sel, clicked)) {
    doAttack(sel, clicked);
    return;
  }
  if (clicked) {
    select(clicked.id === state.selected ? null : clicked);
    refresh();
    return;
  }
  if (sel && state.area && routeTo(state.area, h) && sel.side === g.side) {
    doMove(sel, h);
    return;
  }
  select(null);
  info.textContent = describeHex(h);
  refresh();
}

function endTurn() {
  if (state.busy || state.game.winner || isAiTurn()) return;
  state.game.endTurn();
  select(null);
  autosave();
  refresh();
  runAi();
}

function undo() {
  if (state.busy || isAiTurn() || !state.game.undo()) return;
  const u = selectedUnit();
  if (u) select(u);
  refresh();
}

function nextUnit() {
  const ready = state.game.ready();
  if (!ready.length) return;
  const i = ready.findIndex((u) => u.id === state.selected);
  focusUnit(ready[(i + 1) % ready.length]);
}

// ---------------------------------------------------------------- hover info & forecast tooltip

function describeHex(h) {
  const t = state.game.map.get(h);
  if (!t) return "";
  const tr = terrain(t.terrain);
  const cost = Number.isFinite(tr.cost) ? `move ${tr.cost}` : "impassable";
  return `(${h.q}, ${h.r}) ${tr.name}: ${cost}, defence ${tr.defense}%${tr.blocksSight ? ", blocks sight" : ""}`;
}

const pct = (x) => `${Math.round(x * 100)}%`;

function showTip(ev, html) {
  tip.innerHTML = html;
  tip.hidden = false;
  const box = canvas.parentElement.getBoundingClientRect();
  const x = Math.min(ev.clientX - box.left + 14, box.width - 230);
  tip.style.left = `${Math.max(0, x)}px`;
  tip.style.top = `${ev.clientY - box.top + 14}px`;
}

function hideTip() {
  tip.hidden = true;
}

function updateHover(ev, h) {
  const g = state.game;
  const u = g.unitAt(h);
  const sel = selectedUnit();
  if (u && sel && sel.side === g.side && u.side !== sel.side) {
    const plan = g.attackPlan(sel, u);
    if (plan) {
      const f = plan.forecast;
      const counter = f.counter
        ? `Counter (${f.counter}): ${f.taken.min}–${f.taken.max} dmg, avg ${f.expectedTaken.toFixed(1)}<br>Your death chance: <b>${pct(f.deathChance)}</b>`
        : "No counter-attack";
      showTip(ev, `<b>${f.kind === "melee" ? "Melee" : "Ranged"} attack</b>${f.flank ? ` · flanked ×${f.flank}` : ""}<br>
        Damage ${f.dealt.min}–${f.dealt.max}, avg ${f.expectedDealt.toFixed(1)} (target ${u.hp} HP)<br>
        Kill chance: <b>${pct(f.killChance)}</b><br>${counter}`);
      info.textContent = `${sideName(u.side)} ${describeUnit(u)}`;
      return;
    }
  }
  hideTip();
  if (u) info.textContent = `${sideName(u.side)} ${describeUnit(u)} — on ${terrain(g.map.get(u).terrain).name}`;
  else {
    const node = state.area?.get(key(h));
    info.textContent = describeHex(h) + (node?.canStop && node.cost > 0 ? ` — ${node.cost} MP${node.zoc ? " (enemy zone of control: move ends here)" : ""}` : "");
  }
}

// ---------------------------------------------------------------- events

function local(ev, el = canvas) {
  const r = el.getBoundingClientRect();
  return { x: ev.clientX - r.left, y: ev.clientY - r.top };
}

canvas.addEventListener("mousedown", (ev) => {
  Object.assign(drag, { active: true, moved: false, x: ev.clientX, y: ev.clientY });
});
window.addEventListener("mouseup", (ev) => {
  if (drag.active && !drag.moved && ev.target === canvas) {
    const p = local(ev);
    onClick(hexAtPixel(p.x, p.y, view(state.cam)));
  }
  drag.active = false;
});
canvas.addEventListener("mousemove", (ev) => {
  if (drag.active) {
    const dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
    if (drag.moved || Math.hypot(dx, dy) > 4) {
      drag.moved = true;
      hideTip();
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
  state.hover = state.game.map.has(h) ? h : null;
  if (state.hover) updateHover(ev, h);
  else hideTip();
  if (!state.busy) draw();
});
canvas.addEventListener("mouseleave", () => {
  state.hover = null;
  hideTip();
  draw();
});
canvas.addEventListener("wheel", (ev) => {
  ev.preventDefault();
  hideTip();
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

window.addEventListener("keydown", (ev) => {
  if (ev.target instanceof HTMLInputElement) return;
  if (ev.key === "e" || ev.key === "E") endTurn();
  else if (ev.key === "u" || ev.key === "U" || ((ev.ctrlKey || ev.metaKey) && ev.key === "z")) undo();
  else if (ev.key === "n" || ev.key === "N" || ev.key === "Tab") {
    ev.preventDefault();
    nextUnit();
  } else if (ev.key === "Escape") {
    select(null);
    hideTip();
    refresh();
  } else return;
});

$("newgame").addEventListener("click", () => newBattle(seedInput.value));
$("random").addEventListener("click", () => {
  seedInput.value = String(Math.floor(Math.random() * 1e6));
  newBattle(seedInput.value);
});
$("endturn").addEventListener("click", endTurn);
$("undo").addEventListener("click", undo);
$("zoomreset").addEventListener("click", () => {
  state.cam = camera(state.cam.base);
  draw();
});
$("save").addEventListener("click", () => {
  const s = storage();
  if (!s) return say("Saving needs browser storage, which is blocked here — use Export instead.");
  saveToSlot(s, "manual", state.game);
  say("Game saved (Load restores it).");
});
$("load").addEventListener("click", () => {
  const s = storage();
  const g = s && loadFromSlot(s, "manual");
  if (!g) return say("No saved game yet.");
  setGame(g);
  say("Saved game loaded.");
});
$("export").addEventListener("click", () => {
  const blob = new Blob([serialize(state.game)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `hexfall-${state.game.seed}-turn${state.game.turn}.json`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
});
$("import").addEventListener("change", async (ev) => {
  const file = ev.target.files?.[0];
  if (!file) return;
  try {
    setGame(deserialize(await file.text()));
    say(`Imported ${file.name}.`);
  } catch (err) {
    say(`Import failed: ${err.message}`);
  }
  ev.target.value = "";
});
symInput.addEventListener("change", () => newBattle(seedInput.value));
for (const id of ["redai", "blueai"]) {
  $(id).addEventListener("change", () => {
    setupAi();
    refresh();
    runAi();
  });
}
window.addEventListener("resize", resize);

function say(text) {
  info.textContent = text;
}

// Resume the autosave if the URL has no explicit seed, otherwise start that battle.
(function boot() {
  const pref = readAiPref();
  $("redai").value = pref.red ?? "human";
  $("blueai").value = pref.blue ?? "normal";
  const hash = decodeURIComponent(location.hash.slice(1));
  const s = storage();
  let resumed = null;
  if (!hash && s) {
    try {
      resumed = loadFromSlot(s, "auto");
    } catch {
      resumed = null;
    }
  }
  if (resumed && !resumed.winner) {
    seedInput.value = String(resumed.seed);
    setGame(resumed);
    say("Resumed your last battle (New battle starts over).");
  } else {
    seedInput.value = hash || "1";
    newBattle(seedInput.value);
  }
})();

// Handle for debugging in the console and for the browser smoke test (tests/browser-smoke.mjs).
window.hexfall = { state, view: () => view(state.cam), hexCenter, runAi, setupAi };
