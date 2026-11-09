import test from "node:test";
import assert from "node:assert/strict";
import { importsOf, exportsOf, coverageReport, coverageMarkdown } from "../src/coverage.js";

test("importsOf finds static and dynamic src imports", () => {
  const s = `import {a} from "../src/hex.js";\nconst m = await import("../src/rng.js");\nimport x from "./helpers.js";`;
  assert.deepEqual([...importsOf(s)].sort(), ["hex.js", "rng.js"]);
});
test("exportsOf lists functions, consts and classes", () => {
  const s = `export function f(){}\nexport const G = 1;\nexport class H {}\nexport async function k(){}\nfunction hidden(){}`;
  assert.deepEqual(exportsOf(s), ["f", "G", "H", "k"]);
});
test("coverageReport flags untested modules and unmentioned exports", () => {
  const mods = { "a.js": "export function one(){}\nexport function two(){}", "b.js": "export const x=1;" };
  const tests = { "a.test.js": `import {one} from "../src/a.js"; one();` };
  const r = coverageReport(mods, tests);
  assert.deepEqual(r.untested, ["b.js"]);
  assert.deepEqual(r.partial, ["a.js"]);
  assert.deepEqual(r.rows[0].untestedExports, ["two"]);
});
test("ignore list and markdown output", () => {
  const r = coverageReport({ "a.js": "export const q=1;" }, {}, { ignore: ["a.js"] });
  assert.equal(r.rows.length, 0);
  assert.match(coverageMarkdown(coverageReport({ "z.js": "" }, {})), /Untested modules: z\.js/);
});
