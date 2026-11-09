// Hot-seat curtain without editing main.js: wraps Game.endTurn and covers the board between human turns.
import { Game, SIDES } from "./game.js";
import { Curtain } from "./hotseat.js";

const curtain = new Curtain();
const $ = (id) => document.getElementById(id);
const overlay = document.createElement("div");
overlay.id = "curtain";
overlay.setAttribute("role", "dialog");
overlay.setAttribute("aria-modal", "true");
overlay.hidden = true;
// inline display:flex would override the [hidden] attribute, so toggle display explicitly
overlay.style.cssText = "position:fixed;inset:0;background:#111;color:#eee;display:none;flex-direction:column;align-items:center;justify-content:center;gap:16px;z-index:50;font:18px sans-serif;text-align:center;padding:24px";
const text = document.createElement("p");
const ready = document.createElement("button");
ready.type = "button";
ready.textContent = "Ready";
overlay.append(text, ready);
document.body.append(overlay);

const show = (on) => { overlay.hidden = !on; overlay.style.display = on ? "flex" : "none"; };
ready.addEventListener("click", () => { curtain.reveal(); show(false); });

const origEnd = Game.prototype.endTurn;
Game.prototype.endTurn = function (...args) {
  const res = origEnd.apply(this, args);
  const controllers = [$("redai")?.value ?? "human", $("blueai")?.value ?? "human"];
  if (curtain.arm({ fog: this.rules.fog, controllers, active: this.active, turn: this.turn, winner: this.winner })) {
    text.textContent = curtain.message(SIDES.map((s) => s.name));
    show(true);
    ready.focus();
  }
  return res;
};
