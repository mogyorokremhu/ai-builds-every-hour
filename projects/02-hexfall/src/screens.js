// Menu screens as HTML strings + form parsing + campaign progress storage. DOM-free so it can be tested in node.
import { MAP_SIZES, ARMY_PRESETS, normalizeSetup, setupProblems, armyCost, resolveArmy } from "./skirmish.js";
import { SCENARIOS, newProgress, campaignDone } from "./campaign.js";

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const AI_LEVELS = ["human", "easy", "normal", "hard"];
const opts = (names, cur, label = (n) => n) =>
  names.map((n) => `<option value="${esc(n)}"${n === cur ? " selected" : ""}>${esc(label(n))}</option>`).join("");

/** The skirmish setup form. Field ids are `sk-<name>` so readSkirmishForm can find them. */
export function skirmishHtml(raw = {}, ai = { red: "human", blue: "normal" }) {
  const s = normalizeSetup(raw);
  const armyName = (i) => Object.keys(ARMY_PRESETS).find((k) => ARMY_PRESETS[k].join() === s.armies[i].join()) ?? "standard";
  const row = (label, input) => `<label class="srow"><span>${label}</span>${input}</label>`;
  const problems = setupProblems(s);
  return `<h2>Skirmish setup</h2>
${row("Seed", `<input id="sk-seed" value="${s.seed}" size="8">`)}
${row("Map size", `<select id="sk-size">${opts(Object.keys(MAP_SIZES), s.size, (k) => `${k} (${MAP_SIZES[k].cols}×${MAP_SIZES[k].rows})`)}</select>`)}
${row("Red army", `<select id="sk-army0">${opts(Object.keys(ARMY_PRESETS), armyName(0), (k) => `${k} · ${armyCost(ARMY_PRESETS[k])}g`)}</select>`)}
${row("Blue army", `<select id="sk-army1">${opts(Object.keys(ARMY_PRESETS), armyName(1), (k) => `${k} · ${armyCost(ARMY_PRESETS[k])}g`)}</select>`)}
${row("Red player", `<select id="sk-redai">${opts(AI_LEVELS, ai.red)}</select>`)}
${row("Blue player", `<select id="sk-blueai">${opts(AI_LEVELS, ai.blue)}</select>`)}
${row("Start gold", `<input id="sk-gold" type="number" min="0" max="500" value="${s.startGold}">`)}
${row("Turn limit (0 = none)", `<input id="sk-turns" type="number" min="0" max="60" value="${s.turnLimit}">`)}
${row("Options", `<span><label><input id="sk-fog" type="checkbox"${s.fog ? " checked" : ""}> fog</label>
 <label><input id="sk-weather" type="checkbox"${s.weather ? " checked" : ""}> weather</label>
 <label><input id="sk-sym" type="checkbox"${s.symmetric ? " checked" : ""}> symmetric</label></span>`)}
${problems.length ? `<ul class="problems">${problems.map((p) => `<li>${esc(p)}</li>`).join("")}</ul>` : ""}
<p class="btnrow"><button id="sk-start" class="primary">Start battle</button> <button id="sk-cancel">Cancel</button></p>`;
}

/** Turn raw form values (`{seed, size, army0, ...}` as strings/booleans) into {setup, ai}. */
export function readSkirmishForm(v) {
  const setup = normalizeSetup({
    seed: v.seed, size: v.size, symmetric: !!v.sym, fog: !!v.fog, weather: !!v.weather,
    startGold: v.gold, turnLimit: v.turns,
    armies: [resolveArmy(ARMY_PRESETS[v.army0] ? v.army0 : "standard"), resolveArmy(ARMY_PRESETS[v.army1] ? v.army1 : "standard")],
  });
  const ai = (x, d) => (AI_LEVELS.includes(x) ? x : d);
  return { setup, ai: { red: ai(v.redai, "human"), blue: ai(v.blueai, "normal") } };
}

/** Campaign menu: scenario list with done/current/locked state. */
export function campaignHtml(progress = newProgress()) {
  const items = SCENARIOS.map((sc, i) => {
    const state = i < progress.index ? "done" : i === progress.index ? "current" : "locked";
    const mark = { done: "✔", current: "▶", locked: "🔒" }[state];
    return `<li class="sc ${state}"><b>${mark} ${sc.id}. ${esc(sc.name)}</b> <small>${sc.size} · ${sc.enemyAi} AI${sc.fog ? " · fog" : ""}</small><br><span>${esc(sc.brief)}</span></li>`;
  }).join("");
  const done = campaignDone(progress);
  return `<h2>Campaign</h2><ol class="scenarios">${items}</ol>
<p>${done ? "Campaign complete! " : ""}Won ${progress.won} · lost ${progress.lost} · veterans carried: ${progress.roster.length}</p>
<p class="btnrow">${done ? "" : `<button id="cp-start" class="primary">${progress.won || progress.lost ? "Continue" : "Begin"}: ${esc(SCENARIOS[progress.index].name)}</button> `}
<button id="cp-reset">Restart campaign</button> <button id="cp-close">Close</button></p>`;
}

const KEY = "hexfall.campaign";
/** Load campaign progress from a Storage-like object; falls back to a fresh record on any problem. */
export function loadProgress(storage) {
  try {
    const p = JSON.parse(storage.getItem(KEY));
    if (p && Number.isInteger(p.index) && p.index >= 0 && p.index <= SCENARIOS.length && Array.isArray(p.roster)) {
      return { index: p.index, roster: p.roster, won: p.won | 0, lost: p.lost | 0 };
    }
  } catch { /* fall through */ }
  return newProgress();
}
export function saveProgress(storage, p) {
  try { storage.setItem(KEY, JSON.stringify(p)); } catch { /* optional */ }
}
