#!/usr/bin/env node
// Report which src modules/exports no test touches.   node tools/coverage.mjs [--strict]
import { readdirSync, readFileSync } from "node:fs";
import { coverageReport, coverageMarkdown } from "../src/coverage.js";

const read = (dir, pick) =>
  Object.fromEntries(readdirSync(new URL(dir, import.meta.url)).filter(pick)
    .map((f) => [f, readFileSync(new URL(dir + f, import.meta.url), "utf8")]));
const modules = read("../src/", (f) => f.endsWith(".js"));
const tests = read("../tests/", (f) => f.endsWith(".test.js"));
const report = coverageReport(modules, tests);
console.log(coverageMarkdown(report));
if (process.argv.includes("--strict") && report.untested.length) process.exit(1);
