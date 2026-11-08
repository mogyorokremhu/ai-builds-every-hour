// Focus trap for the menu panel without editing main.js: watches the `hidden` attribute of #panel.
import { trapFocus } from "./focustrap.js";

const panel = document.getElementById("panel");
if (panel) {
  panel.setAttribute("aria-modal", "true");
  let trap = null;
  const sync = () => {
    if (!panel.hidden && !trap) trap = trapFocus(panel);
    else if (panel.hidden && trap) { trap.release(); trap = null; }
  };
  new MutationObserver(sync).observe(panel, { attributes: true, attributeFilter: ["hidden"] });
  sync();
}
