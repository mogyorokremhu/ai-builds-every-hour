// Draws ability animations on a transparent canvas stacked over #board (no main.js edit needed).
import { Game } from "./game.js";
import { installAbilityFx } from "./abilityfxlive.js";
import { drawAbilityEffects } from "./abilityfx.js";

const board = document.getElementById("board");
if (board) {
  const ctl = installAbilityFx(Game);
  const over = document.createElement("canvas");
  over.id = "abilityfx";
  over.setAttribute("aria-hidden", "true");
  over.style.cssText = "position:absolute;pointer-events:none;left:0;top:0";
  board.parentElement.style.position ||= "relative";
  board.after(over);
  let running = false;
  const frame = () => {
    const now = performance.now();
    const w = board.width, h = board.height;
    if (over.width !== w || over.height !== h) { over.width = w; over.height = h; }
    over.style.left = board.offsetLeft + "px"; over.style.top = board.offsetTop + "px";
    over.style.width = board.clientWidth + "px"; over.style.height = board.clientHeight + "px";
    const ctx = over.getContext("2d");
    ctx.clearRect(0, 0, w, h);
    const hf = window.hexfall;
    if (ctl.prune(now) && hf) {
      const dpr = w / (board.clientWidth || w);
      ctx.save(); ctx.scale(dpr, dpr);
      drawAbilityEffects(ctx, ctl.list, now, hf.view());
      ctx.restore();
      requestAnimationFrame(frame);
    } else running = false;
  };
  const kick = () => { if (!running) { running = true; requestAnimationFrame(frame); } };
  const origUse = Game.prototype.useAbility;
  Game.prototype.useAbility = function (...a) { const r = origUse.apply(this, a); kick(); return r; };
}
