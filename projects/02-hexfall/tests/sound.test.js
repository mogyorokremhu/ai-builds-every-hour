import { test } from "node:test";
import assert from "node:assert/strict";
import { SFX, sfxFor, sfxLength, play, setMuted, isMuted } from "../src/sound.js";

test("every recipe is well formed", () => {
  for (const [name, voices] of Object.entries(SFX)) {
    assert.ok(voices.length > 0, name);
    for (const v of voices) {
      assert.ok(v.dur > 0 && v.gain > 0 && v.gain <= 1, name);
      if (v.wave !== "noise") assert.ok(v.from > 0 && v.to > 0, name);
    }
    assert.ok(sfxLength(name) < 1, name);
  }
});

test("sound choice follows the effects", () => {
  const f = (text, heal = false) => ({ kind: "float", text, heal });
  assert.equal(sfxFor([]), null);
  assert.equal(sfxFor([f("-6")]), "hit");
  assert.equal(sfxFor([f("-16")]), "crit");
  assert.equal(sfxFor([f("+8", true), f("-3")]), "heal");
  assert.equal(sfxFor([f("-6"), { kind: "fade" }]), "death");
});

test("play is a harmless no-op without WebAudio and when muted", () => {
  play("hit");
  setMuted(true);
  assert.ok(isMuted());
  play("death");
  setMuted(false);
});
