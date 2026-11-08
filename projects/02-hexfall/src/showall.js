// Show-all fog override installed by spectate-hook.js without editing main.js.
// Patches Game.prototype.visible / isVisible so every viewer sees everything while the flag is on,
// except while an AIPlayer is thinking (the AI must never get free vision).

/** Wrap every prototype method of `AI` so `ctl.depth` is >0 while any of them runs. */
export function guardAI(AI, ctl) {
  for (const name of Object.getOwnPropertyNames(AI.prototype)) {
    const fn = AI.prototype[name];
    if (name === "constructor" || typeof fn !== "function" || fn.__guarded) continue;
    const wrapped = function (...args) {
      ctl.depth++;
      let res;
      try { res = fn.apply(this, args); } finally { ctl.depth--; }
      return res;
    };
    wrapped.__guarded = true;
    AI.prototype[name] = wrapped;
  }
}

/** Install the override; returns a controller { showAll, depth, uninstall }. */
export function installShowAll(GameClass, AI) {
  const ctl = { showAll: false, depth: 0 };
  const origVisible = GameClass.prototype.visible;
  const origIsVisible = GameClass.prototype.isVisible;
  if (AI) guardAI(AI, ctl);
  const active = () => ctl.showAll && ctl.depth === 0;
  GameClass.prototype.visible = function (side) {
    if (!active()) return origVisible.call(this, side);
    if (!this.rules.fog) return null;
    const all = new Set();
    for (const h of this.map) all.add(`${h.q},${h.r}`);
    return all;
  };
  GameClass.prototype.isVisible = function (side, u) {
    return active() ? true : origIsVisible.call(this, side, u);
  };
  ctl.uninstall = () => {
    GameClass.prototype.visible = origVisible;
    GameClass.prototype.isVisible = origIsVisible;
  };
  return ctl;
}
