// Replay viewer logic: step forwards/backwards through a replay file, jump to turns, auto-play.
// Going backwards re-simulates from the start (battles are deterministic and short), so the
// viewer never needs undo support from the game itself.
import { Game } from "./game.js";
import { applyAction, validateReplay, fingerprint } from "./replay.js";

/** A one-line human description of an action; `game` (state before it) names the unit types. */
export function describeAction(game, a) {
  const name = (id) => {
    const u = game?.unitById?.(id);
    return u ? `${u.side} ${u.type}#${u.id}` : `unit#${id}`;
  };
  switch (a.type) {
    case "move": return `${name(a.unitId)} moves to (${a.to.q},${a.to.r})`;
    case "attack": return `${name(a.unitId)} attacks ${name(a.targetId)}`;
    case "ability": return `${name(a.unitId)} uses ${a.ability} at (${a.target.q},${a.target.r})`;
    case "recruit": return `recruits ${a.unitType}${a.at ? ` at (${a.at.q},${a.at.r})` : ""}`;
    case "end": return "ends the turn";
    default: return `unknown action ${a.type}`;
  }
}

export class ReplayViewer {
  constructor(file) {
    const problems = validateReplay(file);
    if (problems.length) throw new Error(`bad replay: ${problems.join("; ")}`);
    this.file = file;
    this.cursor = 0; // number of actions applied so far
    this.timer = null;
    this._reset();
  }

  _reset() {
    this.game = Game.create(structuredClone(this.file.setup));
    this.cursor = 0;
  }

  get length() { return this.file.actions.length; }
  get atStart() { return this.cursor === 0; }
  get atEnd() { return this.cursor >= this.length; }

  /** Description of the action that `step()` would apply next, or null at the end. */
  peek() {
    return this.atEnd ? null : describeAction(this.game, this.file.actions[this.cursor]);
  }

  step() {
    if (this.atEnd) return false;
    applyAction(this.game, this.file.actions[this.cursor]);
    this.cursor++;
    return true;
  }

  back() { return this.seek(this.cursor - 1); }

  /** Move to a position in 0..length by stepping (forward) or re-simulating (backward). */
  seek(n) {
    const target = Math.max(0, Math.min(this.length, Math.floor(n)));
    if (target < this.cursor) this._reset();
    while (this.cursor < target) this.step();
    return this.cursor;
  }

  /** Indices (action counts) at which each turn begins; entry i is the start of turn i + 1. */
  turnStarts() {
    const starts = [0];
    this.file.actions.forEach((a, i) => { if (a.type === "end") starts.push(i + 1); });
    return starts;
  }

  /** Jump to the beginning of turn `t` (1-based; the first side's turn). */
  seekTurn(t) {
    const starts = this.turnStarts();
    return this.seek(starts[Math.max(0, Math.min(starts.length - 1, t - 1))]);
  }

  /** A compact summary of the current position for a status line. */
  summary() {
    const g = this.game;
    const count = (side) => g.units.filter((u) => u.side === side).length;
    return {
      step: this.cursor, of: this.length, turn: g.turn, side: g.side,
      winner: g.winner ?? null, red: count("red"), blue: count("blue"), fingerprint: fingerprint(g),
    };
  }

  /** Auto-play: call `onTick(viewer)` every `ms`; stops at the end. Returns a stop function. */
  play(onTick, ms = 400) {
    this.stop();
    this.timer = setInterval(() => {
      if (!this.step()) { this.stop(); }
      onTick?.(this);
    }, ms);
    return () => this.stop();
  }

  stop() {
    if (this.timer) clearInterval(this.timer);
    this.timer = null;
  }
}
