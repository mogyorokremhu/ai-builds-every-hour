// Browser entry point: a battle on a generated map against the AI or hot-seat — select, move,
// attack, recruit, end turn — plus zoom/pan, minimap, roster, economy panel, day/night strip,
// combat log, damage previews, undo and saves; unit abilities with target previews, status
// effects, weather forecast and optional fog of war.
import { Game, SIDES } from "./game.js";
import { drawMap, drawUnits, fitLayout, hexAtPixel, hexCenter } from "./render.js";
import { routeTo } from "./movement.js";
import { terrain, TERRAIN } from "./terrain.js";
import { terrainCounts } from "./mapgen.js";
import { seedFrom } from "./rng.js";
import { key, neighbors } from "./hex.js";
import { camera, view, zoomAt, panBy, visibleRect, centerOn, clamp } from "./camera.js";
import { describeUnit, unitType, maxHp, maxMp, RECRUITABLE, UNIT_TYPES } from "./units.js";
import { AIPlayer, DIFFICULTY } from "./ai.js";
import { ownedVillages, income } from "./economy.js";
import { upcoming } from "./timeofday.js";
import { moveAnimation, lungeAnimation, animatedPosition, finished } from "./animate.js";
import { serialize, deserialize, saveToSlot, loadFromSlot } from "./save.js";
import { ABILITIES, abilitiesOf, abilityPreview, abilityStatus } from "./abilities.js";
import { weatherForecast } from "./weather.js";
import { describeStatuses, statusLabel } from "./status.js";

const $ = (id) => document.getElementById(id);
const canvas = $("board");
const ctx = canvas.getContext("2d");
const mini = $("minimap");
const mctx = mini.getContext("2d");
const info = $("info");
const tip = $("tip");
const seedInput = $("seed");
const symInput = $("sym");
const fogInput = $("fog");
const weatherInput = $("weather");

const state = {
  game: null, cam: null, viewport: { width: 0, height: 0 }, miniLayout: null,
  selected: null, area: null, hover: null, anims: [], busy: false,
  ability: null, // ability id being aimed by the selected unit
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
  setGame(Game.create({
    seed: parseSeed(seedText), symmetric: symInput.checked,
    rules: { fog: fogInput.checked, weather: weatherInput.checked },
  }));
  location.hash = encodeURIComponent(seedText);
}

function setGame(game) {
  state.game = game;
  fogInput.checked = !!game.rules.fog;
  weatherInput.checked = game.rules.weather !== false;
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

/**
 * Whose eyes the board is drawn through under fog of war: the human side to move, else the
 * only human side, else nobody (AI vs AI spectators and fog-free battles see everything).
 */
function viewerSide() {
  const g = state.game;
  if (!g.rules.fog || g.winner) return null;
  if (!state.ai[g.side]) return g.side;
  const humans = SIDES.filter((s) => !state.ai[s.id]);
  return humans.length === 1 ? humans[0].id : null;
}

/** The unit on `h` if the viewer can see it. */
function visibleUnitAt(h) {
  const u = state.game.unitAt(h);
  const viewer = viewerSide();
  return u && (!viewer || state.game.isVisible(viewer, u)) ? u : null;
}

function abilityTargetsOf(u) {
  return state.ability && u ? state.game.abilityTargets(u, state.ability) : [];
}

function draw(now = performance.now()) {
  const g = state.game;
  const layout = view(state.cam);
  const sel = selectedUnit();
  const overlay = {
    spawns: g.turn === 1 && g.active === 0 ? g.spawns : [], hover: state.hover, tint: g.timeOfDay().tint,
    weatherTint: g.weather().tint,
    recruit: state.recruitMode && !isAiTurn() ? g.recruitHexes() : [],
  };
  const viewer = viewerSide();
  if (viewer) {
    overlay.visible = g.visible(viewer);
    overlay.explored = g.explored[g.sideIndex(viewer)];
  }
  if (sel && state.ability && !state.busy) {
    overlay.selected = sel;
    overlay.abilityTargets = abilityTargetsOf(sel);
    if (state.ability === "fireball" && state.hover && overlay.abilityTargets.some((h) => key(h) === key(state.hover))) {
      overlay.blast = [state.hover, ...neighbors(state.hover)];
    }
  } else if (sel && state.area && !state.busy) {
    overlay.reach = new Map([...state.area].filter(([, n]) => n.canStop));
    overlay.selected = sel;
    overlay.targets = g.units.filter((t) => t.side !== sel.side && g.attackPlan(sel, t));
    const hoverUnit = state.hover && visibleUnitAt(state.hover);
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
  const isVisible = viewer ? (u) => g.isVisible(viewer, u) : null;
  drawUnits(ctx, g.units, layout, { selected: state.selected, positions, activeSide: g.side, isVisible });
  drawMinimap();
}

function drawMinimap() {
  const g = state.game;
  const viewer = viewerSide();
  const fog = viewer ? { visible: g.visible(viewer), explored: g.explored[g.sideIndex(viewer)] } : {};
  drawMap(mctx, g.map, state.miniLayout, fog);
  drawUnits(mctx, g.units, state.miniLayout, { isVisible: viewer ? (u) => g.isVisible(viewer, u) : null });
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
  renderAbilities();
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
    const viewer = viewerSide();
    const shown = g.unitsOf(side.id).filter((u) => !viewer || g.isVisible(viewer, u));
    const n = g.unitsOf(side.id).length;
    const v = ownedVillages(g, side.id).length;
    const count = shown.length === n ? `${n} unit${n === 1 ? "" : "s"}` : `${shown.length} seen`;
    head.textContent = `${side.name}${state.ai[side.id] ? " (AI)" : ""} — ${count} · ⚑ ${v}`;
    ul.append(head);
    for (const u of shown) {
      const li = document.createElement("li");
      li.className = `runit ${side.id}${u.id === state.selected ? " sel" : ""}${side.id === g.side && (u.acted || u.mp <= 0) ? " spent" : ""}`;
      li.tabIndex = 0;
      const pct = Math.round((u.hp / maxHp(u)) * 100);
      li.innerHTML = `<b>${unitType(u).glyph}</b> ${unitType(u).name}${"★".repeat(u.level - 1)}
        <span class="hp"><i style="width:${pct}%"></i></span><small>${u.hp}/${maxHp(u)} · ${u.mp}/${maxMp(u)} MP${statusLabel(u) ? ` · ${statusLabel(u)}` : ""}</small>`;
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
  const weather = weatherForecast(g, 6);
  $("daynight").innerHTML = upcoming(g.turn, 6).map((p, i) =>
    `<span class="tod${i === 0 ? " now" : ""}" title="Turn ${p.turn}: ${p.name} — lawful ${p.lawful >= 0 ? "+" : ""}${p.lawful}%, chaotic ${p.lawful <= 0 ? "+" : ""}${-p.lawful}%; ${weather[i].name}: ${weather[i].text}">${p.icon}<small>${weather[i].id === "clear" ? "" : weather[i].icon}</small></span>`).join("")
    + `<span class="wx" title="${weather[0].text}">${weather[0].icon} ${weather[0].name}${g.rules.fog ? " · fog of war" : ""}</span>`;
}

/** Ability buttons for the selected unit (when it is the human side's turn). */
function renderAbilities() {
  const g = state.game;
  const el = $("abilities");
  el.innerHTML = "";
  const u = selectedUnit();
  if (!u || u.side !== g.side || isAiTurn() || g.winner) {
    el.hidden = true;
    return;
  }
  el.hidden = false;
  abilitiesOf(u).forEach((id, i) => {
    const ab = ABILITIES[id];
    const status = abilityStatus(g, u, id);
    const b = document.createElement("button");
    b.className = `abtn${state.ability === id ? " on" : ""}`;
    b.disabled = status !== "ready" || state.busy;
    b.title = `${ab.text} [${status}] — key ${i + 1}`;
    b.innerHTML = `${ab.icon} ${ab.name} <small>${status === "ready" ? (ab.cooldown ? `cooldown ${ab.cooldown}` : "") : status}</small>`;
    b.addEventListener("click", () => toggleAbility(id));
    el.append(b);
  });
}

function toggleAbility(id) {
  const g = state.game;
  const u = selectedUnit();
  if (!u || state.busy || isAiTurn() || abilityStatus(g, u, id) !== "ready") return;
  if (ABILITIES[id].target === "self") {
    doAbility(u, id, { q: u.q, r: u.r });
    return;
  }
  state.ability = state.ability === id ? null : id;
  hideTip();
  refresh();
}

function renderLog() {
  const el = $("log");
  el.innerHTML = state.game.log.slice(-40).map((l) => `<li class="${l.side}">${escapeHtml(l.text)}</li>`).join("");
  el.scrollTop = el.scrollHeight;
}

function renderUnitInfo() {
  const u = selectedUnit();
  const st = u ? describeStatuses(u) : [];
  $("unitinfo").textContent = u ? `${sideName(u.side)} ${describeUnit(u)} — ${unitType(u).blurb}${st.length ? ` Status: ${st.join("; ")}` : ""}` : "";
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
      } else if (a.type === "attack" || a.type === "ability") {
        const t = a.type === "attack" ? g.unitById(a.targetId) : a.target;
        if (key(a.from) !== key(u)) {
          const route = routeTo(g.area(u), a.from);
          if (route) await animate([moveAnimation(u.id, route, performance.now())]);
        }
        if (key(t) !== key(a.from)) await animate([lungeAnimation(u.id, a.from, t, performance.now())]);
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
  state.ability = null;
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

async function doAbility(u, id, target) {
  const g = state.game;
  if (key(target) !== key(u)) await animate([lungeAnimation(u.id, u, target, performance.now())]);
  g.useAbility(u, id, target);
  select(null);
  autosave();
  refresh();
}

function onClick(h) {
  const g = state.game;
  if (state.busy || isAiTurn()) return;
  hideTip();
  const clicked = visibleUnitAt(h);
  const sel = selectedUnit();
  if (sel && state.ability) {
    const id = state.ability;
    if (abilityTargetsOf(sel).some((t) => key(t) === key(h))) doAbility(sel, id, h);
    else {
      state.ability = null;
      refresh();
    }
    return;
  }
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
  const viewer = viewerSide();
  const fogged = viewer && !state.game.visible(viewer).has(key(h)) ? " (not in sight)" : "";
  return `(${h.q}, ${h.r}) ${tr.name}: ${cost}, defence ${tr.defense}%${tr.blocksSight ? ", blocks sight" : ""}${t.fire > 0 ? `, burning (${t.fire} turns: +2 MP, 6 damage)` : ""}${fogged}`;
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

function abilityTip(sel, h) {
  const p = abilityPreview(state.game, sel, state.ability, h);
  if (!p) return null;
  const ab = ABILITIES[state.ability];
  const lines = [`<b>${ab.icon} ${ab.name}</b>`];
  for (const hit of p.hits) {
    const own = hit.unit.side === sel.side ? " <i>(ally!)</i>" : "";
    lines.push(`${unitType(hit.unit).name}${own}: ${hit.min}–${hit.max} dmg, kill ${pct(hit.killChance)}`);
  }
  if (p.counter) lines.push(`Counter: avg ${p.counter.expected.toFixed(1)}, your death chance <b>${pct(p.counter.deathChance)}</b>`);
  else if (p.hits.length) lines.push("No counter-attack");
  if (p.heal || p.cures) lines.push(`Heals ${p.heal}${p.cures ? ", cures poison" : ""}`);
  if (p.fires) lines.push(`${p.fires} hex${p.fires === 1 ? "" : "es"} catch fire`);
  return lines.join("<br>");
}

function updateHover(ev, h) {
  const g = state.game;
  const u = visibleUnitAt(h);
  const sel = selectedUnit();
  if (sel && state.ability) {
    const html = abilityTip(sel, h);
    if (html) showTip(ev, html);
    else hideTip();
    info.textContent = describeHex(h);
    return;
  }
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
  } else if (/^[1-9]$/.test(ev.key)) {
    const u = selectedUnit();
    const id = u && abilitiesOf(u)[Number(ev.key) - 1];
    if (id) toggleAbility(id);
  } else if (ev.key === "Escape") {
    if (state.ability) {
      state.ability = null;
      hideTip();
      refresh();
      return;
    }
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
fogInput.addEventListener("change", () => newBattle(seedInput.value));
weatherInput.addEventListener("change", () => newBattle(seedInput.value));
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
