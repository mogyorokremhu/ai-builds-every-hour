// Balance analysis over self-play series: per-unit efficiency, side bias and flags.
// Pure functions on the object returned by runSeries(); no game state needed.
import { UNIT_TYPES } from "./units.js";

/**
 * Per unit type: recruits, kills, kills per recruit and kills per 100 gold spent.
 * @returns {Array<{id:string, name:string, cost:number, recruits:number, kills:number, perRecruit:number, per100Gold:number}>}
 */
export function unitEfficiency(series) {
  const rows = [];
  for (const [id, t] of Object.entries(UNIT_TYPES)) {
    const recruits = series.recruits[id] ?? 0;
    const kills = series.kills[id] ?? 0;
    const gold = recruits * t.cost;
    rows.push({
      id, name: t.name, cost: t.cost, recruits, kills,
      perRecruit: recruits ? kills / recruits : 0,
      per100Gold: gold ? (kills / gold) * 100 : 0,
    });
  }
  return rows;
}

/** Side bias: red's share of decided games and a z-score against a fair coin. */
export function sideBias(series) {
  const decided = series.wins.red + series.wins.blue;
  if (!decided) return { decided: 0, redShare: 0.5, z: 0 };
  const redShare = series.wins.red / decided;
  const z = (series.wins.red - decided / 2) / Math.sqrt(decided / 4);
  return { decided, redShare, z };
}

/**
 * Human-readable warnings: units far above/below the median efficiency (per 100 gold),
 * units never recruited, a significant side bias, and games that end by timeout.
 */
export function balanceFlags(series, { tolerance = 0.5 } = {}) {
  const flags = [];
  const rows = unitEfficiency(series).filter((r) => r.recruits > 0);
  const sorted = rows.map((r) => r.per100Gold).sort((a, b) => a - b);
  const median = sorted.length ? sorted[Math.floor(sorted.length / 2)] : 0;
  for (const r of rows) {
    if (median > 0 && r.per100Gold > median * (1 + tolerance)) flags.push(`${r.name} overperforms (${r.per100Gold.toFixed(1)} kills/100g vs median ${median.toFixed(1)})`);
    if (median > 0 && r.per100Gold < median * (1 - tolerance)) flags.push(`${r.name} underperforms (${r.per100Gold.toFixed(1)} kills/100g vs median ${median.toFixed(1)})`);
  }
  for (const [id, t] of Object.entries(UNIT_TYPES)) {
    if (!(series.recruits[id] > 0)) flags.push(`${t.name} was never recruited`);
  }
  const bias = sideBias(series);
  if (Math.abs(bias.z) >= 1.96) flags.push(`side bias: red won ${(bias.redShare * 100).toFixed(0)}% of ${bias.decided} decided games (z=${bias.z.toFixed(2)})`);
  const timeouts = (series.reasons.turns ?? 0) + (series.wins.none ?? 0);
  if (timeouts / series.games > 0.2) flags.push(`${timeouts} of ${series.games} games hit the turn limit`);
  return flags;
}

/** Markdown section for BALANCE.md. */
export function balanceMarkdown(series, title) {
  const bias = sideBias(series);
  const lines = [
    `### ${title}`, "",
    `${series.games} games, avg ${series.avgTurns.toFixed(1)} turns. Red ${series.wins.red} – blue ${series.wins.blue}` +
      ` (red share ${(bias.redShare * 100).toFixed(0)}%, z=${bias.z.toFixed(2)}). End reasons: ${Object.entries(series.reasons).map(([k, v]) => `${k} ${v}`).join(", ")}.`,
    "", "| Unit | Cost | Recruited | Kills | Kills/recruit | Kills/100g |", "|---|---|---|---|---|---|",
  ];
  for (const r of unitEfficiency(series)) lines.push(`| ${r.name} | ${r.cost} | ${r.recruits} | ${r.kills} | ${r.perRecruit.toFixed(2)} | ${r.per100Gold.toFixed(1)} |`);
  const abil = Object.entries(series.abilities ?? {}).sort((a, b) => b[1] - a[1]);
  if (abil.length) lines.push("", `Ability uses: ${abil.map(([k, v]) => `${k} ${v}`).join(", ")}.`);
  const flags = balanceFlags(series);
  lines.push("", flags.length ? "Flags:" : "Flags: none.", ...flags.map((f) => `- ${f}`), "");
  return lines.join("\n");
}
