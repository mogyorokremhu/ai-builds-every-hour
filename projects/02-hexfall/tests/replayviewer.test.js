import { test } from "node:test";
import assert from "node:assert/strict";
import { recordAIMatch, fingerprint } from "../src/replay.js";
import { ReplayViewer, describeAction } from "../src/replayviewer.js";

const file = recordAIMatch({ seed: 5, rules: { turnLimit: 6 } });

test("stepping to the end reproduces the recorded fingerprint", () => {
  const v = new ReplayViewer(file);
  assert.ok(v.atStart);
  v.seek(v.length);
  assert.ok(v.atEnd);
  assert.equal(fingerprint(v.game), file.result.fingerprint);
  assert.equal(v.step(), false);
});

test("seeking backwards re-simulates to the same state as going forward", () => {
  const v = new ReplayViewer(file);
  const mid = Math.floor(v.length / 2);
  v.seek(mid);
  const fp = fingerprint(v.game);
  v.seek(v.length);
  v.seek(mid);
  assert.equal(fingerprint(v.game), fp);
  assert.equal(v.back(), mid - 1);
});

test("seek clamps out-of-range positions", () => {
  const v = new ReplayViewer(file);
  assert.equal(v.seek(-5), 0);
  assert.equal(v.seek(1e9), v.length);
});

test("turn starts follow the end actions and seekTurn lands on them", () => {
  const v = new ReplayViewer(file);
  const starts = v.turnStarts();
  assert.equal(starts[0], 0);
  assert.equal(starts.length, file.actions.filter((a) => a.type === "end").length + 1);
  v.seekTurn(2);
  assert.equal(v.cursor, starts[1]);
  assert.equal(v.seekTurn(999), starts[starts.length - 1]);
});

test("descriptions and summary are readable", () => {
  const v = new ReplayViewer(file);
  assert.match(v.peek(), /\w/);
  assert.equal(describeAction(null, { type: "end" }), "ends the turn");
  assert.match(describeAction(v.game, { type: "move", unitId: 1, to: { q: 2, r: 3 } }), /\(2,3\)/);
  const s = v.summary();
  assert.equal(s.step, 0);
  assert.equal(s.of, file.actions.length);
});

test("bad replay files are rejected and play() stops at the end", async () => {
  assert.throws(() => new ReplayViewer({ version: 99 }));
  const small = { ...file, actions: file.actions.slice(0, 3) };
  const v = new ReplayViewer(small);
  await new Promise((res) => { v.play(() => { if (v.atEnd) res(); }, 1); });
  await new Promise((r) => setTimeout(r, 10));
  assert.equal(v.timer, null);
  assert.equal(v.cursor, 3);
});
