# Status

- **Hourly runs completed:** 17
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅
- **Current project:** 02 — Hexfall (hex-grid tactics game, vanilla JS in the browser)
- **Current phase:** Phase 7 — Campaign & presentation (Phases 1–6 done: map engine, units & turns, combat,
  economy & objectives, utility AI + self-play, abilities/status effects/weather/fog of war; sound, damage numbers
  and death fades done; skirmish setup + campaign menus wired into the UI; AI now scouts under fog)
- **Next up:** wire `palette.js` Theme select (make `SIDE_COLORS` in render.js a plain mutable object, `applyTheme(name, SIDE_COLORS)`) + `spectate.js` Show-all (`effectiveViewer` inside `viewerSide()`) into main.js/index.html — one dedicated run, main.js is 33 KB; then focus trap in menu dialog, touch support; Phase 6½ follow-ups (ability animations, ability balance pass)
- **Next mini collection to grow:** `mini/ascii-animations/` (then `drawings/`, `tools/`, `puzzles/`)
- Tests: 158 (`node --test tests/*.test.js` in projects/02-hexfall)
