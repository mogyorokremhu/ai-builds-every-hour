// Replay files: a battle is fully determined by its setup (seed, map options, rules, armies)
// plus the list of player actions, so a replay is just those two things. Re-simulating the
// actions on a fresh Game reproduces the battle exactly; a state fingerprint detects drift.
import { Game } from "./game.js";
import { AIPlayer } from "./ai.js";

export const REPLAY_VERSION = 1;

/** A short deterministic fingerprint (FNV-1a) of the parts of a game that matter. */
export function fingerprint(game) {
  const s = JSON.stringify([
    game.turn, game.active, game.winner, game.gold,
    game.units.map((u) => [u.id, u.type, u.side, u.q, u.r, u.hp, u.xp]),
  ]);
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 0x01000193) >>> 0;
  return h.toString(16).padStart(8, "0");
}

/** Records primitive actions applied to a game: move, attack, ability, recruit, end. */
export class Recorder {
  constructor(setup = {}) {
    this.setup = structuredClone(setup);
    this.actions = [];
  }

  /** Apply a primitive action to `game` and record it if it was accepted. */
  apply(game, action) {
    const res = applyAction(game, action);
    if (res !== false) this.actions.push(structuredClone(action));
    return res;
  }

  /**
   * Log every top-level move/attack/ability/recruit call made on `game` from now on (an AI can
   * then play normally). Returns a function that removes the hooks.
   */
  watch(game) {
    let depth = 0;
    const originals = {};
    const hooks = {
      move: (u, to) => ({ type: "move", unitId: u.id, to: { q: to.q, r: to.r } }),
      attack: (u, t) => ({ type: "attack", unitId: u.id, targetId: t.id }),
      useAbility: (u, ability, target) => ({ type: "ability", unitId: u.id, ability, target: { q: target.q, r: target.r } }),
      recruit: (unitType, at) => ({ type: "recruit", unitType, at: at ? { q: at.q, r: at.r } : null }),
    };
    for (const [name, describe] of Object.entries(hooks)) {
      originals[name] = game[name];
      game[name] = (...args) => {
        const action = describe(...args);
        depth++;
        try {
          const res = originals[name].apply(game, args);
          if (depth === 1) this.actions.push(action);
          return res;
        } finally {
          depth--;
        }
      };
    }
    return () => { for (const name of Object.keys(originals)) delete game[name]; };
  }

  /** Finish: the plain-object replay file. */
  finish(game) {
    return {
      version: REPLAY_VERSION,
      setup: this.setup,
      actions: this.actions,
      result: { winner: game.winner, turn: game.turn, fingerprint: fingerprint(game) },
    };
  }
}

/** Apply one primitive action; returns false when the game rejects it (it throws on bad moves). */
export function applyAction(game, action) {
  try {
    switch (action.type) {
      case "recruit": return game.recruit(action.unitType, action.at ?? null);
      case "move": {
        const u = game.unitById(action.unitId);
        return u ? game.move(u, action.to) : false;
      }
      case "attack": {
        const u = game.unitById(action.unitId);
        const t = game.unitById(action.targetId);
        return u && t ? game.attack(u, t) : false;
      }
      case "ability": {
        const u = game.unitById(action.unitId);
        return u ? game.useAbility(u, action.ability, action.target) : false;
      }
      case "end":
        if (game.winner) return false;
        game.endTurn();
        return true;
      default:
        return false;
    }
  } catch {
    return false;
  }
}

/** Check that an object looks like a replay file; returns a list of problems. */
export function validateReplay(replay) {
  const problems = [];
  if (!replay || typeof replay !== "object") return ["not an object"];
  if (replay.version !== REPLAY_VERSION) problems.push(`unsupported version ${replay.version}`);
  if (!replay.setup || typeof replay.setup !== "object") problems.push("missing setup");
  if (!Array.isArray(replay.actions)) problems.push("missing actions");
  else replay.actions.forEach((a, i) => { if (!a || typeof a.type !== "string") problems.push(`action ${i} has no type`); });
  return problems;
}

/**
 * Re-simulate a replay. `onStep(game, action, index)` is called after every action, which a
 * viewer can use to animate. Returns {game, applied, rejected, matches}.
 */
export function replay(file, { onStep } = {}) {
  const problems = validateReplay(file);
  if (problems.length) throw new Error(`bad replay: ${problems.join("; ")}`);
  const game = Game.create(structuredClone(file.setup));
  let applied = 0;
  let rejected = 0;
  file.actions.forEach((action, i) => {
    if (applyAction(game, action) === false) rejected++;
    else applied++;
    onStep?.(game, action, i);
  });
  const matches = !file.result || file.result.fingerprint === fingerprint(game);
  return { game, applied, rejected, matches };
}

/** Play a whole AI-vs-AI battle while recording it; returns the replay file. */
export function recordAIMatch(setup = {}, { difficulties = ["normal", "normal"], maxTurns } = {}) {
  const seed = setup.seed ?? 1;
  const full = { symmetric: true, ...setup, seed };
  const game = Game.create(structuredClone(full));
  const rec = new Recorder(full);
  const players = {
    red: new AIPlayer("red", { difficulty: difficulties[0], seed }),
    blue: new AIPlayer("blue", { difficulty: difficulties[1], seed: seed * 7 + 3 }),
  };
  const limit = maxTurns ?? (game.rules.turnLimit || 60) + 1;
  const unwatch = rec.watch(game);
  let guard = 0;
  while (!game.winner && game.turn <= limit && guard++ < limit * 4) {
    const p = players[game.side];
    for (let i = 0; i < 300; i++) {
      const a = p.nextAction(game);
      if (a.type === "end") break;
      p.play(game, a);
      if (game.winner) break;
    }
    if (!game.winner) rec.apply(game, { type: "end" });
  }
  unwatch();
  return rec.finish(game);
}
