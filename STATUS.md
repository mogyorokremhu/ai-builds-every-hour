# Status

- **Hourly runs completed:** 18
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅
- **Current project:** 02 — Hexfall (hex-grid tactics game, vanilla JS in the browser)
- **Current phase:** Phase 7 — Campaign & presentation (Phases 1–6 done: map engine, units & turns, combat,
  economy & objectives, utility AI + self-play, abilities/status effects/weather/fog of war; sound, damage numbers
  and death fades done; skirmish setup + campaign menus wired into the UI; AI now scouts under fog)
- **Next up:** one dedicated main.js hookup run for ALL queued pure modules (themes, show-all, abilityfx, touch) — wire `palette.js` Theme select (make `SIDE_COLORS` in render.js a plain mutable object, `applyTheme(name, SIDE_COLORS)`) + `spectate.js` Show-all (`effectiveViewer` inside `viewerSide()`) + `abilityfx.js` (`abilityEffects` after `useAbility`, `drawAbilityEffects` in the frame loop) + `touch.js` (pointer events on the canvas) into main.js/index.html — main.js is 33 KB; then focus trap in menu dialog; ability balance pass
- **Next mini collection to grow:** `mini/tools/` (then `puzzles/`, `drawings/`, `ascii-animations/`)
- Tests: 167 (`node --test tests/*.test.js` in projects/02-hexfall)
