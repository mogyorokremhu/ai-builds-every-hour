// Live ability animations without editing main.js: wraps Game.prototype.useAbility and queues
// abilityfx.js effects into a list that abilityfx-hook.js draws on an overlay canvas.
import { abilityEffects, progress } from "./abilityfx.js";
import { neighbors } from "./hex.js";

/** Hexes hit by a volley: the target plus every adjacent unit not on the caster's side. */
export function volleyVictims(game, unit, target) {
  const out = [{ q: target.q, r: target.r }];
  for (const n of neighbors(target)) {
    const v = game.unitAt?.(n);
    if (v && v.side !== unit.side) out.push({ q: n.q, r: n.r });
  }
  return out;
}

/**
 * Install the wrapper. `ctl.list` collects effects; `ctl.now` supplies the clock (injectable for tests).
 * Returns { list, seed, now, prune(now), uninstall() }.
 */
export function installAbilityFx(GameClass, now = () => performance.now()) {
  const orig = GameClass.prototype.useAbility;
  const ctl = { list: [], seed: 1, now, orig };
  GameClass.prototype.useAbility = function (unit, id, target) {
    const at = target ?? unit;
    const info = { id, target: at };
    if (id === "volley") info.victims = volleyVictims(this, unit, at);
    const res = orig.call(this, unit, id, target);
    try {
      ctl.list.push(...abilityEffects(info, ctl.now(), ctl.seed++));
    } catch { /* animation must never break the game */ }
    return res;
  };
  ctl.prune = (t) => { ctl.list = ctl.list.filter((f) => t <= f.start + f.duration); return ctl.list.length; };
  ctl.active = (t) => ctl.list.some((f) => progress(f, t) !== null);
  ctl.uninstall = () => { GameClass.prototype.useAbility = orig; };
  return ctl;
}
