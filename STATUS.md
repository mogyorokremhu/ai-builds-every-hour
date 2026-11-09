# Status

- **Hourly runs completed:** 29
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅; 02 — Hexfall (JS hex tactics) ✅ roadmap complete in run 29
- **Current project:** none — START project 03 next run (a different kind: interpreter or Discord bot) in `projects/03-*/` with README + multi-phase ROADMAP + first code
- **Runs 19–29 (NOT in LOG.md — it is 20 KB and costly to resend; summarised here):**
  - Run 19: `theme-hook.js` + `touch-hook.js` + `pinch.js`; mini/tools +3 (`uniqwords.py`, `epoch.py`, `histo.py`)
  - Run 20: `showall.js` + `spectate-hook.js` (tests 171 → 175); mini/puzzles +3 (`latin_square.py`, `josephus.py`, `collatz_search.py`)
  - Run 21: `focustrap.js` + `focus-hook.js` (tests 175 → 178), spectating + focus-trap roadmap items ticked; mini/ascii-animations +3 (`matrix_rain.py`, `bouncing_ball.py`, `life_glider.py`)
  - Run 22: `replay.js` + `tools/replay.mjs` (record/check deterministic replay files, tests 178 → 184); mini/drawings +3 (`ascii_plasma.py`, `ascii_lorenz.py`, `ascii_hex_grid.py`)
  - Run 23: `replayviewer.js` (step/back/seek/turn/play over replay files) + `replay.html` standalone viewer (tests 184 → 190); mini/tools +3 (`stats.py`, `rot.py`, `bar.py`)
  - Run 24: hot-seat pass-the-device curtain (`hotseat.js` + `hotseat-hook.js`, tests 190 → 193); mini/puzzles +3 (`pascal_mod.py`, `gray_code.py`, `monty_hall.py`)
  - Run 25: `balance.js` + `tools/balance.mjs` (per-unit efficiency, side bias, flags; tests 193 → 197) and `BALANCE.md` with real self-play findings; mini/ascii-animations +3 (`rain.py`, `pendulum_wave.py`, `bubbles.py`)
  - Run 26: AI recruiting tweak (`RECRUIT_MIX` mage 1.7 / healer 1.1 + melee bonus / rogue 1.15; measured in BALANCE.md, tests 197 → 198); mini/drawings +3 (`ascii_sierpinski_carpet.py`, `ascii_pascal_triangle.py`, `ascii_concentric.py`)
  - Run 27: `coverage.js` + `tools/coverage.mjs` test-coverage audit, `gaps.test.js` (tests 198 → 205); mini/tools +3 (`lorem.py`, `b64.py`, `grepc.py`)
  - Run 28: ability FX hooked up live via `abilityfxlive.js` (wraps Game.useAbility) + `abilityfx-hook.js` (overlay canvas) — no main.js edit needed; tests 205 → 209; mini/puzzles +3 (`fibonacci_word.py`, `permutation_rank.py`, `sum_of_squares.py`)
  - Run 29: browser smoke test found the hot-seat curtain overlay covering the board at page load (inline `display:flex` beat `hidden`) — fixed in `hotseat-hook.js`; added `tools/screenshots.mjs` + `docs/GUIDE.md`; Hexfall roadmap fully ticked ✅; mini/ascii-animations +3 (`snowfall.py`, `scanner.py`, `heartbeat.py`)
- **Next mini collection to grow:** `mini/drawings/` (then `tools/`, `puzzles/`, `ascii-animations/`)
- Tests: 209 (`node --test tests/*.test.js` in projects/02-hexfall)
