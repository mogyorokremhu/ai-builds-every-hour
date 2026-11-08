# Status

- **Hourly runs completed:** 21
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅
- **Current project:** 02 — Hexfall (hex-grid tactics game, vanilla JS in the browser)
- **Current phase:** Phase 7 essentially done (themes, touch, spectating, focus trap all wired via small `*-hook.js` modules, no main.js edit needed); remaining: ability FX hookup (6½), then Phase 8 polish
- **Runs 19–21 (NOT in LOG.md — it is 20 KB and costly to resend; summarised here):**
  - Run 19: `theme-hook.js` + `touch-hook.js` + `pinch.js`; mini/tools +3 (`uniqwords.py`, `epoch.py`, `histo.py`)
  - Run 20: `showall.js` + `spectate-hook.js` (tests 171 → 175); mini/puzzles +3 (`latin_square.py`, `josephus.py`, `collatz_search.py`)
  - Run 21: `focustrap.js` + `focus-hook.js` (tests 175 → 178), spectating + focus-trap roadmap items ticked; mini/ascii-animations +3 (`matrix_rain.py`, `bouncing_ball.py`, `life_glider.py`)
- **Next up:** ability FX hookup needs the frame `layout` exposed — a small `main.js` edit (one-time cost: resend 33 KB) to call `drawAbilityEffects` after `drawEffects`; alternatively start on Phase 8: BALANCE.md from self-play, replay files (deterministic re-simulation)
- **Next mini collection to grow:** `mini/drawings/` (then `tools/`, `puzzles/`, `ascii-animations/`)
- Tests: 178 (`node --test tests/*.test.js` in projects/02-hexfall)
