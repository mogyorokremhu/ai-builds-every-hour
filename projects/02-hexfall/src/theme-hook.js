// Theme select without editing main.js: recolours SIDE_COLORS (render.js) and asks main.js to redraw via a resize event.
import { THEMES, applyTheme } from "./palette.js";
import { SIDE_COLORS } from "./render.js";

const KEY = "hexfall.theme";
const read = () => { try { return localStorage.getItem(KEY) || "default"; } catch { return "default"; } };
const write = (v) => { try { localStorage.setItem(KEY, v); } catch { /* storage may be blocked */ } };

const host = document.querySelector("header, .toolbar, body");
const sound = document.getElementById("sound");
const label = document.createElement("label");
label.textContent = "Theme ";
const sel = document.createElement("select");
sel.id = "theme";
sel.setAttribute("aria-label", "Colour theme");
for (const [id, t] of Object.entries(THEMES)) sel.add(new Option(t.label, id));
label.append(sel);
(sound?.closest("label") ?? host).after?.(label) ?? host.append(label);

const set = (name) => {
  const t = applyTheme(name, SIDE_COLORS);
  sel.value = THEMES[name] ? name : "default";
  document.documentElement.style.setProperty("--red", t.red);
  document.documentElement.style.setProperty("--blue", t.blue);
  write(sel.value);
  window.dispatchEvent(new Event("resize")); // main.js redraws on resize
};
sel.addEventListener("change", () => set(sel.value));
set(read());
