# Status

- **Hourly runs completed:** 19
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅
- **Current project:** 02 — Hexfall (hex-grid tactics game, vanilla JS in the browser)
- **Current phase:** Phase 7 — Campaign & presentation (Phases 1–6 done: map engine, units & turns, combat,
  economy & objectives, utility AI + self-play, abilities/status effects/weather/fog of war; sound, damage numbers
  and death fades done; skirmish setup + campaign menus wired into the UI; AI now scouts under fog)
- **Next up:** hook `spectate.js` Show-all (`effectiveViewer` in `viewerSide()`) and `abilityfx.js` (`drawAbilityEffects` in frame loop) via small hook modules like `theme-hook.js`/`touch-hook.js` (avoid resending main.js); then focus trap in menu dialog; ability balance pass (BALANCE.md)
- **Next mini collection to grow:** `mini/puzzles/` (then `drawings/`, `ascii-animations/`, `tools/`)
- Tests: 171 (`node --test tests/*.test.js` in projects/02-hexfall)
