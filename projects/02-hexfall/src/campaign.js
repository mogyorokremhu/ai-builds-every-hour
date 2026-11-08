// A five-scenario campaign. Survivors of a won scenario return as veterans (keeping levels, perks and bonuses).
import { createUnit, UNIT_TYPES } from "./units.js";

export const SCENARIOS = Object.freeze([
  { id: 1, name: "The Border Skirmish", seed: 11, size: "small", enemy: ["swordsman", "spearman", "archer"], enemyAi: "easy",
    gold: 60, turnLimit: 14, fog: false, weather: false, player: ["swordsman", "spearman", "archer", "healer"],
    brief: "Drive off a raiding party before nightfall." },
  { id: 2, name: "Ford of Ashes", seed: 23, size: "small", enemy: ["swordsman", "swordsman", "archer", "cavalry"], enemyAi: "easy",
    gold: 70, turnLimit: 16, fog: false, weather: true, player: [], brief: "Hold the river crossing. Your veterans return." },
  { id: 3, name: "Night Watch", seed: 37, size: "medium", enemy: ["spearman", "archer", "archer", "mage", "cavalry"], enemyAi: "normal",
    gold: 80, turnLimit: 18, fog: true, weather: true, player: [], brief: "Fog hides the enemy camp; scout carefully." },
  { id: 4, name: "The Mage Tower", seed: 41, size: "medium", enemy: ["mage", "mage", "spearman", "spearman", "healer", "cavalry"], enemyAi: "normal",
    gold: 90, turnLimit: 20, fog: false, weather: true, player: [], brief: "Break the sorcerers before they burn the forest." },
  { id: 5, name: "Hexfall", seed: 59, size: "large", enemy: ["swordsman", "swordsman", "spearman", "archer", "mage", "healer", "cavalry"],
    enemyAi: "hard", gold: 120, turnLimit: 24, fog: true, weather: true, player: [], brief: "The final battle. Everyone who is left fights." },
]);

/** Reduce a won battle's survivors to a roster of plain records worth carrying over. */
export function carryOver(game, side = "red") {
  return game.unitsOf(side).filter((u) => u.hp > 0).map((u) => ({
    type: u.type, xp: u.xp, level: u.level, kills: u.kills, perks: [...u.perks], bonus: { ...u.bonus },
  }));
}

/** Put a carried-over roster onto `game` for `side` (veterans first), restoring full health. */
export function restoreVeterans(game, side, roster) {
  const zone = game.spawns[game.sideIndex(side)].filter((h) => !game.unitAt(h) && game.map.passable(h));
  const placed = [];
  roster.slice(0, zone.length).forEach((rec, i) => {
    if (!UNIT_TYPES[rec.type]) return;
    const u = createUnit(game.nextId++, rec.type, side, zone[i]);
    Object.assign(u, { xp: rec.xp, level: rec.level, kills: rec.kills, perks: [...rec.perks], bonus: { ...u.bonus, ...rec.bonus } });
    u.hp += rec.bonus?.hp ?? 0;
    game.units.push(u);
    placed.push(u);
  });
  return placed;
}

/** Game.create() options for scenario `index` (0-based). The player's side is red. */
export function scenarioOptions(index) {
  const sc = SCENARIOS[index];
  if (!sc) throw new Error(`no scenario ${index}`);
  const size = { small: [18, 12, 4, 5], medium: [24, 16, 6, 6], large: [32, 20, 8, 7] }[sc.size];
  return {
    seed: sc.seed, symmetric: false, armies: [sc.player, sc.enemy],
    map: { cols: size[0], rows: size[1], villages: size[2], spawnSize: size[3] },
    rules: { fog: sc.fog, weather: sc.weather, startGold: sc.gold, turnLimit: sc.turnLimit },
  };
}

/** Progress record for saving; `advance` returns the next one after a win (or the same one after a loss). */
export function newProgress() { return { index: 0, roster: [], won: 0, lost: 0 }; }
export function advance(progress, game) {
  if (game.winner !== "red") return { ...progress, lost: progress.lost + 1 };
  return { index: Math.min(progress.index + 1, SCENARIOS.length), roster: carryOver(game), won: progress.won + 1, lost: progress.lost };
}
export const campaignDone = (p) => p.index >= SCENARIOS.length;
