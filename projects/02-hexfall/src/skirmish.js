// Skirmish setup: validate a user-chosen configuration and turn it into Game.create() options. DOM-free.
import { UNIT_TYPES, DEFAULT_ARMY } from "./units.js";

export const MAP_SIZES = Object.freeze({
  small: { cols: 18, rows: 12, villages: 4, spawnSize: 5 },
  medium: { cols: 24, rows: 16, villages: 6, spawnSize: 6 },
  large: { cols: 32, rows: 20, villages: 8, spawnSize: 7 },
});
export const ARMY_PRESETS = Object.freeze({
  standard: DEFAULT_ARMY,
  cavalry: ["cavalry", "cavalry", "cavalry", "archer", "healer"],
  ranged: ["archer", "archer", "mage", "mage", "spearman", "spearman", "healer"],
  infantry: ["swordsman", "swordsman", "spearman", "spearman", "spearman", "healer"],
});
export const LIMITS = Object.freeze({ gold: [0, 500], turns: [0, 60], armySize: [1, 8] });

export const DEFAULT_SETUP = Object.freeze({
  seed: 1, size: "medium", symmetric: false, fog: false, weather: true,
  startGold: 100, turnLimit: 0, armies: ["standard", "standard"],
});

const clamp = (n, [lo, hi]) => Math.min(hi, Math.max(lo, Math.round(Number(n))));
const num = (v, fallback) => (Number.isFinite(Number(v)) && v !== "" && v !== null ? Number(v) : fallback);

/** Total recruit cost of a list of unit types. */
export const armyCost = (types) => types.reduce((s, t) => s + UNIT_TYPES[t].cost, 0);

/** Resolve an army spec (preset name or explicit type list) to a list of unit types. */
export function resolveArmy(spec) {
  const list = typeof spec === "string" ? ARMY_PRESETS[spec] : spec;
  if (!Array.isArray(list)) throw new Error(`unknown army ${JSON.stringify(spec)}`);
  for (const t of list) if (!UNIT_TYPES[t]) throw new Error(`unknown unit type ${t}`);
  return [...list];
}

/** Clamp every field into its legal range and fill in defaults. Never throws on bad numbers. */
export function normalizeSetup(raw = {}) {
  const s = { ...DEFAULT_SETUP, ...raw };
  const size = MAP_SIZES[s.size] ? s.size : "medium";
  const armies = [0, 1].map((i) => {
    const spec = Array.isArray(s.armies) ? s.armies[i] : undefined;
    try { return resolveArmy(spec ?? "standard"); } catch { return [...ARMY_PRESETS.standard]; }
  }).map((a) => a.slice(0, LIMITS.armySize[1]));
  return {
    seed: Math.max(0, Math.floor(num(s.seed, 1))), size,
    symmetric: !!s.symmetric, fog: !!s.fog, weather: s.weather !== false,
    startGold: clamp(num(s.startGold, 100), LIMITS.gold),
    turnLimit: clamp(num(s.turnLimit, 0), LIMITS.turns),
    armies,
  };
}

/** Human-readable problems with a (normalised) setup, e.g. an army too big for the deployment zone. */
export function setupProblems(setup) {
  const s = normalizeSetup(setup);
  const zone = MAP_SIZES[s.size].spawnSize;
  const out = [];
  s.armies.forEach((a, i) => {
    if (a.length > zone) out.push(`Side ${i + 1}: ${a.length} units but a ${s.size} map deploys only ${zone}`);
  });
  const diff = Math.abs(armyCost(s.armies[0]) - armyCost(s.armies[1]));
  if (diff > 30) out.push(`Armies differ by ${diff} gold of value`);
  return out;
}

/** Game.create() options for a setup (armies are trimmed to the deployment zone so creation never throws). */
export function toGameOptions(setup) {
  const s = normalizeSetup(setup);
  const { cols, rows, villages, spawnSize } = MAP_SIZES[s.size];
  return {
    seed: s.seed, symmetric: s.symmetric,
    armies: s.armies.map((a) => a.slice(0, spawnSize)),
    map: { cols, rows, villages, spawnSize },
    rules: { fog: s.fog, weather: s.weather, startGold: s.startGold, turnLimit: s.turnLimit },
  };
}
