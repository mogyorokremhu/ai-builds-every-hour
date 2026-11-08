// Sound effects synthesised with WebAudio — no asset files. Recipes are plain data so they can be tested.

/** Each recipe: list of voices {wave, from, to (Hz sweep), dur (s), gain, delay (s)} or noise bursts. */
export const SFX = Object.freeze({
  hit:    [{ wave: "square", from: 220, to: 70, dur: 0.12, gain: 0.25 }, { wave: "noise", dur: 0.08, gain: 0.3 }],
  crit:   [{ wave: "sawtooth", from: 320, to: 60, dur: 0.2, gain: 0.3 }, { wave: "noise", dur: 0.14, gain: 0.35 }],
  heal:   [{ wave: "sine", from: 523, to: 523, dur: 0.12, gain: 0.25 }, { wave: "sine", from: 784, to: 784, dur: 0.18, gain: 0.25, delay: 0.1 }],
  death:  [{ wave: "triangle", from: 300, to: 40, dur: 0.5, gain: 0.35 }],
  move:   [{ wave: "noise", dur: 0.03, gain: 0.12 }],
  select: [{ wave: "sine", from: 660, to: 880, dur: 0.06, gain: 0.15 }],
  coin:   [{ wave: "square", from: 988, to: 988, dur: 0.07, gain: 0.15 }, { wave: "square", from: 1319, to: 1319, dur: 0.14, gain: 0.15, delay: 0.07 }],
  fire:   [{ wave: "noise", dur: 0.35, gain: 0.35 }, { wave: "sawtooth", from: 140, to: 50, dur: 0.35, gain: 0.2 }],
  turn:   [{ wave: "triangle", from: 392, to: 392, dur: 0.1, gain: 0.2 }, { wave: "triangle", from: 523, to: 523, dur: 0.16, gain: 0.2, delay: 0.1 }],
});

/** Which sound goes with a floating-number effect list (death beats heal beats hit). */
export function sfxFor(effects) {
  if (!effects.length) return null;
  if (effects.some((e) => e.kind === "fade")) return "death";
  if (effects.some((e) => e.kind === "float" && e.heal)) return "heal";
  const worst = Math.min(...effects.filter((e) => e.kind === "float").map((e) => Number(e.text)));
  return worst <= -15 ? "crit" : "hit";
}

/** Total length of a recipe in seconds. */
export const sfxLength = (name) => Math.max(...SFX[name].map((v) => (v.delay ?? 0) + v.dur));

let ctx = null, muted = false;
export const isMuted = () => muted;
export const setMuted = (m) => { muted = !!m; };

/** Play a named effect. Safe to call anywhere: silently does nothing without WebAudio or when muted. */
export function play(name) {
  if (muted || !SFX[name]) return;
  try {
    ctx ??= new (globalThis.AudioContext ?? globalThis.webkitAudioContext)();
    if (ctx.state === "suspended") ctx.resume();
    const t0 = ctx.currentTime;
    for (const v of SFX[name]) {
      const t = t0 + (v.delay ?? 0);
      const g = ctx.createGain();
      g.gain.setValueAtTime(v.gain, t);
      g.gain.exponentialRampToValueAtTime(0.0001, t + v.dur);
      g.connect(ctx.destination);
      let src;
      if (v.wave === "noise") {
        const n = Math.max(1, Math.floor(ctx.sampleRate * v.dur));
        const buf = ctx.createBuffer(1, n, ctx.sampleRate), d = buf.getChannelData(0);
        for (let i = 0; i < n; i++) d[i] = Math.random() * 2 - 1;
        src = ctx.createBufferSource();
        src.buffer = buf;
      } else {
        src = ctx.createOscillator();
        src.type = v.wave;
        src.frequency.setValueAtTime(v.from, t);
        src.frequency.exponentialRampToValueAtTime(Math.max(1, v.to), t + v.dur);
      }
      src.connect(g);
      src.start(t);
      src.stop(t + v.dur + 0.02);
    }
  } catch { /* no audio available */ }
}
