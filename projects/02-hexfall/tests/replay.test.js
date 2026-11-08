import { test } from "node:test";
import assert from "node:assert/strict";
import { recordAIMatch, replay, validateReplay, fingerprint, Recorder, applyAction } from "../src/replay.js";
import { Game } from "../src/game.js";

const rec = recordAIMatch({ seed: 4, rules: { turnLimit: 8 } });

test("a recorded AI match replays to the identical state", () => {
  assert.ok(rec.actions.length > 10);
  const r = replay(rec);
  assert.equal(r.rejected, 0);
  assert.ok(r.matches);
  assert.equal(r.game.turn, rec.result.turn);
});

test("replay files survive a JSON round trip", () => {
  const r = replay(JSON.parse(JSON.stringify(rec)));
  assert.ok(r.matches);
});

test("tampering with the actions is detected", () => {
  const bad = structuredClone(rec);
  const i = bad.actions.findIndex((a) => a.type === "attack");
  assert.ok(i >= 0);
  bad.actions.splice(i, 1);
  const r = replay(bad);
  assert.ok(!r.matches || r.rejected > 0);
});

test("onStep fires once per action", () => {
  let n = 0;
  replay(rec, { onStep: () => n++ });
  assert.equal(n, rec.actions.length);
});

test("validateReplay reports problems", () => {
  assert.deepEqual(validateReplay(rec), []);
  assert.ok(validateReplay({ version: 9, actions: [{}] }).length >= 3);
  assert.throws(() => replay({}), /bad replay/);
});

test("Recorder.apply skips rejected actions and fingerprints differ by state", () => {
  const game = Game.create({ seed: 2, symmetric: true });
  const r = new Recorder({ seed: 2, symmetric: true });
  assert.equal(r.apply(game, { type: "move", unitId: 99999, to: { q: 0, r: 0 } }), false);
  assert.equal(r.actions.length, 0);
  const f0 = fingerprint(game);
  assert.ok(r.apply(game, { type: "end" }));
  assert.notEqual(fingerprint(game), f0);
  assert.equal(applyAction(game, { type: "bogus" }), false);
});
