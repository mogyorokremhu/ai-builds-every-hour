#!/usr/bin/env node
// Record and verify replay files.
//   node tools/replay.mjs record out.json [--seed 3] [--turns 20] [--red normal] [--blue hard]
//   node tools/replay.mjs check  out.json     (re-simulates, exits 1 if the result differs)
import { readFileSync, writeFileSync } from "node:fs";
import { recordAIMatch, replay } from "../src/replay.js";

const [cmd, file] = process.argv.slice(2);
const arg = (n, d) => { const i = process.argv.indexOf(`--${n}`); return i >= 0 ? process.argv[i + 1] : d; };

if (cmd === "record" && file) {
  const seed = Number(arg("seed", 1));
  const rep = recordAIMatch({ seed, rules: { turnLimit: Number(arg("turns", 20)) } }, { difficulties: [arg("red", "normal"), arg("blue", "normal")] });
  writeFileSync(file, JSON.stringify(rep));
  console.log(`recorded ${rep.actions.length} actions, winner ${rep.result.winner ?? "none"} after ${rep.result.turn} turns -> ${file}`);
} else if (cmd === "check" && file) {
  const r = replay(JSON.parse(readFileSync(file, "utf8")));
  console.log(`applied ${r.applied}, rejected ${r.rejected}, fingerprint ${r.matches ? "matches" : "DIFFERS"}`);
  process.exit(r.matches && r.rejected === 0 ? 0 : 1);
} else {
  console.log("usage: replay.mjs record <file> [--seed N] | check <file>");
  process.exit(2);
}
