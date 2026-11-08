#!/usr/bin/env node
// AI vs AI balance harness.
//   node tools/selfplay.mjs [--games 20] [--start 1] [--red normal] [--blue normal] [--asym] [--turns 30] [--json]
import { runSeries, formatReport } from "../src/selfplay.js";

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 && i + 1 < process.argv.length ? process.argv[i + 1] : fallback;
}
const flag = (name) => process.argv.includes(`--${name}`);

const games = Number(arg("games", 20));
const start = Number(arg("start", 1));
const difficulties = [arg("red", "normal"), arg("blue", "normal")];
const turnLimit = Number(arg("turns", 30));
const t0 = Date.now();
const series = runSeries({ games, start, difficulties, symmetric: !flag("asym"), rules: { turnLimit } });
if (flag("json")) {
  console.log(JSON.stringify(series, null, 2));
} else {
  console.log(formatReport(series, `${difficulties[0]} (red) vs ${difficulties[1]} (blue)`));
  console.log(`  ${((Date.now() - t0) / 1000).toFixed(1)} s`);
}
