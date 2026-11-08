import test from "node:test";
import assert from "node:assert/strict";
import { THEMES, luminance, contrastRatio, nextTheme, applyTheme } from "../src/palette.js";
import { effectiveViewer, toggleLabel, needsConfirm } from "../src/spectate.js";

test("luminance extremes", () => {
  assert.equal(luminance("#000000"), 0);
  assert.ok(Math.abs(luminance("#ffffff") - 1) < 1e-9);
});
test("contrast ratio black/white is 21", () => {
  assert.ok(Math.abs(contrastRatio("#000000", "#ffffff") - 21) < 1e-6);
  assert.equal(contrastRatio("#123456", "#123456"), 1);
});
test("high-contrast side colours differ strongly from each other and outline", () => {
  const t = THEMES.contrast;
  assert.ok(contrastRatio(t.red, t.blue) > 1.3);
  assert.ok(contrastRatio(t.red, t.outline) >= 3);
  assert.ok(contrastRatio(t.blue, t.outline) >= 3);
});
test("non-default themes keep red and blue distinguishable by luminance", () => {
  for (const [name, t] of Object.entries(THEMES).filter(([n]) => n !== "default")) assert.ok(contrastRatio(t.red, t.blue) > 1.1, name);
});
test("nextTheme cycles", () => {
  assert.equal(nextTheme("default"), "contrast");
  assert.equal(nextTheme("colorblind"), "default");
  assert.equal(nextTheme("???"), "default");
});
test("applyTheme mutates target, unknown falls back", () => {
  const c = { red: "x", blue: "y" };
  applyTheme("colorblind", c);
  assert.equal(c.red, THEMES.colorblind.red);
  applyTheme("nope", c);
  assert.equal(c.blue, THEMES.default.blue);
});
test("spectate helpers", () => {
  assert.equal(effectiveViewer("red", true), null);
  assert.equal(effectiveViewer("red", false), "red");
  assert.equal(toggleLabel(false, true), "Show all (fog off)");
  assert.equal(toggleLabel(true, true), "Fog: showing all");
  assert.equal(needsConfirm(2, false), true);
  assert.equal(needsConfirm(1, false), false);
  assert.equal(needsConfirm(2, true), false);
});
