import { test } from "node:test";
import assert from "node:assert/strict";
import { nextIndex, wouldEscape, trapFocus } from "../src/focustrap.js";

test("nextIndex wraps in both directions", () => {
  assert.equal(nextIndex(2, 3), 0);
  assert.equal(nextIndex(0, 3, true), 2);
  assert.equal(nextIndex(1, 3), 2);
  assert.equal(nextIndex(-1, 3), 0);
  assert.equal(nextIndex(-1, 3, true), 2);
  assert.equal(nextIndex(0, 0), -1);
});

test("wouldEscape only at the edges or outside", () => {
  assert.equal(wouldEscape(1, 3), false);
  assert.equal(wouldEscape(2, 3), true);
  assert.equal(wouldEscape(0, 3, true), true);
  assert.equal(wouldEscape(-1, 3), true);
  assert.equal(wouldEscape(0, 0), false);
});

test("trapFocus cycles focus using a fake DOM", () => {
  const mk = (n) => ({ n, hidden: false, focus() { doc.activeElement = this; } });
  const els = [mk(1), mk(2), mk(3)];
  const doc = { activeElement: null };
  let handler;
  const root = {
    querySelectorAll: () => els,
    addEventListener: (_, f) => { handler = f; },
    removeEventListener: () => { handler = null; },
  };
  const t = trapFocus(root, doc);
  assert.equal(doc.activeElement, els[0]);
  els[2].focus();
  let prevented = false;
  handler({ key: "Tab", shiftKey: false, preventDefault: () => { prevented = true; } });
  assert.ok(prevented);
  assert.equal(doc.activeElement, els[0]);
  t.release();
  assert.equal(handler, null);
});
