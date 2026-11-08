// Colour themes: default, high-contrast and colour-blind-safe (Okabe–Ito). Pure data + helpers so it is testable.

export const THEMES = Object.freeze({
  default:   { label: "Default",           red: "#d0473f", blue: "#3f74d0", outline: "#000000", dim: 0 },
  contrast:  { label: "High contrast",     red: "#ff3b30", blue: "#00b7ff", outline: "#000000", dim: 0.15 },
  colorblind:{ label: "Colour-blind safe", red: "#d55e00", blue: "#0072b2", outline: "#ffffff", dim: 0.05 },
});

/** Relative luminance of a #rrggbb colour (WCAG). */
export function luminance(hex) {
  const n = parseInt(hex.slice(1), 16);
  const ch = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => {
    const s = v / 255;
    return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2];
}

/** WCAG contrast ratio between two colours, 1..21. */
export function contrastRatio(a, b) {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

/** Name of the next theme in the cycle after `name` (unknown names restart at default). */
export function nextTheme(name) {
  const names = Object.keys(THEMES);
  return names[(names.indexOf(name) + 1) % names.length];
}

/** Mutates `target` ({red, blue}) to the theme's side colours; returns the theme. Unknown name → default. */
export function applyTheme(name, target) {
  const t = THEMES[name] ?? THEMES.default;
  target.red = t.red;
  target.blue = t.blue;
  return t;
}
