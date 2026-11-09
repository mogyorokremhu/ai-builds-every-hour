#!/usr/bin/env node
// Run self-play series and print a BALANCE.md-style markdown report.
//   node tools/balance.mjs [--games 20] [--start 1] [--turns 30]
import { runSeries } from "../src/selfplay.js";
import { balanceMarkdown } from "../src/balance.js";

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 && i + 1 < process.argv.length ? process.argv[i + 1] : fallback;
}
const games = Number(arg("games", 20));
const start = Number(arg("start", 1));
const rules = { turnLimit: Number(arg("turns", 30)) };
for (const [r, b] of [["normal", "normal"], ["hard", "easy"]]) {
  const s = runSeries({ games, start, difficulties: [r, b], rules });
  console.log(balanceMarkdown(s, `${r} (red) vs ${b} (blue)`));
}
