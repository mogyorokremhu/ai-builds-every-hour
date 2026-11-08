# Status

- **Hourly runs completed:** 19
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅
- **Current project:** 02 — Hexfall (hex-grid tactics game, vanilla JS in the browser)
- **Current phase:** Phase 7 — Campaign & presentation (Phases 1–6 done; themes (Theme select) and touch support now wired via `theme-hook.js` / `touch-hook.js`, no main.js edit needed)
- **Run 19 (not yet in LOG.md — append it next run, LOG.md is 20 KB so it is costly to resend):** Hexfall `theme-hook.js` + `touch-hook.js` + `pinch.js` (tests 167 → 171), `SIDE_COLORS` made mutable, roadmap themes + touch ticked; mini/tools +3: `uniqwords.py`, `epoch.py`, `histo.py`
- **Next up:** hook `spectate.js` Show-all (`effectiveViewer` in `viewerSide()`) and `abilityfx.js` (`drawAbilityEffects` in frame loop) via small hook modules like `theme-hook.js`; then focus trap in menu dialog; ability balance pass (BALANCE.md)
- **Next mini collection to grow:** `mini/puzzles/` (then `drawings/`, `ascii-animations/`, `tools/`)
- Tests: 171 (`node --test tests/*.test.js` in projects/02-hexfall)
