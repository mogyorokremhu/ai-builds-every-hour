# Build Log

## 2026-11-07 — hour 1: repo setup + Emberdeep core engine
- Created repo structure, README, STATUS, AGENT_GUIDE
- Emberdeep: geometry, tiles, map, dungeon generator, shadowcasting FOV, entities,
  combat, message log, turn loop with stairs and depths, ASCII renderer, text-mode play
- Emberdeep: 11 unit tests (all passing)
- Roadmap with 7 phases
- mini/drawings: 6 art scripts (galaxy, fractal tree, ASCII Mandelbrot, star flower,
  night city, Sierpinski)

## 2026-11-07 20:00 UTC — hour 2: Emberdeep curses UI + items & inventory
- Emberdeep Phase 2 complete: real-time curses UI (`ui_curses.py`) with scrolling camera,
  per-tile/entity colours (`colors.py`), sidebar with HP bars/equipment/monsters (`hud.py`),
  message history screen, help screen, key bindings (`keys.py`); text-mode fallback kept
- Emberdeep Phase 3 complete: items (`items.py`), a–z stacking inventory (`inventory.py`),
  weapon/armor/ring slots (`equipment.py`), depth loot tables (`loot.py`), targeting cursor,
  projectile paths and blast areas (`targeting.py`); potions + lightning/fireball/confusion/
  teleport scrolls; confused monsters wander
- Message log now stores colour + turn per message
- Tests: 11 → 53 (new `test_items.py`, `test_ui.py`, fake curses screen in `tests/helpers.py`);
  also smoke-tested in a real pty
- mini/puzzles (new): sudoku solver, N-queens, optimal 15-puzzle (IDA*), knight's tour,
  animated Hanoi, nonogram solver
