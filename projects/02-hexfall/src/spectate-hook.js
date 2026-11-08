// "Show all" fog toggle without editing main.js: patches Game visibility (see showall.js) and redraws via resize.
import { Game } from "./game.js";
import { AIPlayer } from "./ai.js";
import { installShowAll } from "./showall.js";
import { toggleLabel } from "./spectate.js";

const ctl = installShowAll(Game, AIPlayer);
const fogInput = document.getElementById("fog");
const btn = document.createElement("button");
btn.id = "showall";
btn.type = "button";
btn.setAttribute("aria-pressed", "false");
const refresh = () => {
  btn.textContent = toggleLabel(!!fogInput?.checked, ctl.showAll);
  btn.setAttribute("aria-pressed", String(ctl.showAll));
};
btn.addEventListener("click", () => {
  ctl.showAll = !ctl.showAll;
  refresh();
  window.dispatchEvent(new Event("resize"));
});
fogInput?.addEventListener("change", () => { ctl.showAll = false; refresh(); });
(fogInput?.closest("label") ?? document.body).after?.(btn);
refresh();
