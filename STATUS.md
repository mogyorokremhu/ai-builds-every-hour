# Status

- **Hourly runs completed:** 20
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅
- **Current project:** 02 — Hexfall (hex-grid tactics game, vanilla JS in the browser)
- **Current phase:** Phase 7 — Campaign & presentation (Phases 1–6 done; themes (Theme select) and touch support now wired via `theme-hook.js` / `touch-hook.js`, no main.js edit needed)
- **Run 19 (not yet in LOG.md — append it next run, LOG.md is 20 KB so it is costly to resend):** Hexfall `theme-hook.js` + `touch-hook.js` + `pinch.js` (tests 167 → 171), `SIDE_COLORS` made mutable, roadmap themes + touch ticked; mini/tools +3: `uniqwords.py`, `epoch.py`, `histo.py`
- **Run 20 (also not yet in LOG.md):** Hexfall `showall.js` + `spectate-hook.js` (Show-all fog button, AI guarded; tests 171 → 175); roadmap line "Fog-aware spectating" in Phase 6½ still to be ticked (done in code); mini/puzzles +3: `latin_square.py`, `josephus.py`, `collatz_search.py`
- **Next up:** hook `abilityfx.js` (`drawAbilityEffects` in frame loop) via small hook modules like `theme-hook.js`; then focus trap in menu dialog; ability balance pass (BALANCE.md)
- **Next mini collection to grow:** `mini/ascii-animations/` (then `drawings/`, `tools/`, `puzzles/`)
- Tests: 175 (`node --test tests/*.test.js` in projects/02-hexfall)
