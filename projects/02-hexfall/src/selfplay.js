// AI vs AI self-play: run whole battles headless (node or browser) and gather statistics
// for balance testing. `node tools/selfplay.mjs --games 40` prints a report.
import { Game } from "./game.js";
import { AIPlayer } from "./ai.js";
import { unitType } from "./units.js";

/**
 * Play one battle to the end with both sides controlled by the AI.
 * @param {object} [opts] {seed, symmetric, difficulties: [red, blue], rules, map, maxTurns}
 * @returns {{seed:number, winner:string|null, reason:string|null, turns:number, units:object,
 *   recruits:Record<string, number>, kills:Record<string, number>, villages:object, game: Game}}
 */
export function runMatch(opts = {}) {
  const seed = opts.seed ?? 1;
  const game = Game.create({ seed, symmetric: opts.symmetric ?? true, rules: opts.rules, map: opts.map });
  const [dr, db] = opts.difficulties ?? ["normal", "normal"];
  const players = { red: new AIPlayer("red", { difficulty: dr, seed }), blue: new AIPlayer("blue", { difficulty: db, seed: seed * 7 + 3 }) };
  const recruits = {};
  const kills = {};
  const abilities = {};
  const maxTurns = opts.maxTurns ?? (game.rules.turnLimit || 60) + 1;
  let guard = 0;
  while (!game.winner && game.turn <= maxTurns && guard++ < maxTurns * 4) {
    const p = players[game.side];
    for (let i = 0; i < 300; i++) {
      const a = p.nextAction(game);
      if (a.type === "end") break;
      const res = p.play(game, a);
      if (a.type === "recruit") recruits[a.unitType] = (recruits[a.unitType] ?? 0) + 1;
      if (a.type === "ability" && res) {
        abilities[a.ability] = (abilities[a.ability] ?? 0) + 1;
        const user = game.unitById(a.unitId);
        if (user) for (const id of res.killed) if (id !== a.unitId) kills[user.type] = (kills[user.type] ?? 0) + 1;
      }
      if (a.type === "attack" && res) {
        const attacker = game.unitById(a.unitId);
        for (const id of res.killed) {
          if (id === a.targetId && attacker) kills[attacker.type] = (kills[attacker.type] ?? 0) + 1;
        }
      }
      if (game.winner) break;
    }
    if (!game.winner) game.endTurn();
  }
  const survivors = {};
  for (const u of game.units) survivors[u.side] = (survivors[u.side] ?? 0) + 1;
  return {
    seed, winner: game.winner, reason: game.endReason, turns: game.turn,
    units: survivors, recruits, kills, abilities,
    villages: Object.fromEntries(["red", "blue"].map((s) => [s, game.villages.filter((v) => game.map.get(v)?.owner === s).length])),
    game,
  };
}

/**
 * Run many matches (seeds start..start+games-1) and aggregate win rates, end reasons,
 * battle length and per-unit-type recruits and kills.
 */
export function runSeries({ games = 20, start = 1, ...opts } = {}) {
  const wins = { red: 0, blue: 0, draw: 0, none: 0 };
  const reasons = {};
  const recruits = {};
  const kills = {};
  const abilities = {};
  let turns = 0;
  const results = [];
  for (let s = start; s < start + games; s++) {
    const r = runMatch({ ...opts, seed: s });
    results.push({ seed: s, winner: r.winner, reason: r.reason, turns: r.turns });
    wins[r.winner ?? "none"] += 1;
    reasons[r.reason ?? "unfinished"] = (reasons[r.reason ?? "unfinished"] ?? 0) + 1;
    turns += r.turns;
    for (const [k, v] of Object.entries(r.recruits)) recruits[k] = (recruits[k] ?? 0) + v;
    for (const [k, v] of Object.entries(r.kills)) kills[k] = (kills[k] ?? 0) + v;
    for (const [k, v] of Object.entries(r.abilities)) abilities[k] = (abilities[k] ?? 0) + v;
  }
  return { games, wins, reasons, avgTurns: turns / games, recruits, kills, abilities, results };
}

/** A plain-text report of a runSeries() result. */
export function formatReport(series, label = "") {
  const pct = (n) => `${((n / series.games) * 100).toFixed(1)}%`;
  const lines = [
    `Hexfall self-play${label ? ` — ${label}` : ""}: ${series.games} games, avg ${series.avgTurns.toFixed(1)} turns`,
    `  wins: red ${series.wins.red} (${pct(series.wins.red)}), blue ${series.wins.blue} (${pct(series.wins.blue)}), draw ${series.wins.draw}, unfinished ${series.wins.none}`,
    `  end reasons: ${Object.entries(series.reasons).map(([k, v]) => `${k} ${v}`).join(", ")}`,
    "  unit type    recruited  kills",
  ];
  const types = new Set([...Object.keys(series.recruits), ...Object.keys(series.kills)]);
  for (const t of [...types].sort()) {
    lines.push(`  ${unitType(t).name.padEnd(12)} ${String(series.recruits[t] ?? 0).padStart(9)}  ${String(series.kills[t] ?? 0).padStart(5)}`);
  }
  const used = Object.entries(series.abilities ?? {});
  if (used.length) lines.push(`  abilities used: ${used.sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${v}`).join(", ")}`);
  return lines.join("\n");
}
