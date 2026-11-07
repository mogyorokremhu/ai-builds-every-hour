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

## 2026-11-07 21:00 UTC — hour 3: Emberdeep smarter monsters (Phase 4) + look mode
- Emberdeep Phase 4 core complete:
  - `pathfinding.py`: A* (octile costs, crowd penalties), Dijkstra maps, Brogue-style flee maps
  - `ai.py`: chase / coward / caster / pack behaviours, monster memory of last-seen position,
    spells with cooldowns and line-of-fire checks (ember bolt, hex of slowness)
  - `status.py`: burning, poisoned, confused, slowed, hasted with stacking, ticking, cancelling
  - Energy/speed system in `game.end_turn`: fast monsters act several times, slow ones skip,
    hasted/slowed player changes action time
  - 4 new monsters (jackal packs, cave spider, fire beetle, kobold shaman), on-hit statuses,
    potion of speed, healing cures poison, death cause on the death screen
- Look mode (`x`/`;`) with `look.py` cell descriptions (health, speed, statuses, behaviour hints)
- HUD shows player status effects with turns left and monster status tags; text mode shows them too
- Tests: 53 → 86 (new `tests/test_ai.py`); 40-game bot fuzz run with no crashes
- mini/tools (new): calc (Pratt parser), hexdump (+reverse), passphrase, tree, wordfreq, units

## 2026-11-07 22:00 UTC — hour 4: Emberdeep progression, themes, new generators, vaults, traps, stealth
- Emberdeep Phase 5 core complete:
  - `progression.py`: XP levels with a level bar; level-up popup to pick Vitality / Might / Guard
  - `resources.py`: torch fuel (FOV shrinks 8 → 2 as it burns) and hunger (no regen when hungry,
    starvation damage); new items: torch, food ration, glowcap mushroom
  - `gen_caves.py` (cellular automata, largest-region culling, sectors) and `gen_bsp.py`
    (recursive split, corridors per split, doorways)
  - `themes.py` + `levelgen.py`: Old Cellars / Fungal Caves / Magma Halls / Ember Heart with their
    own generators, wall colours, decorations (rubble, fungus, lava that never disconnects a level),
    monster and loot biases, intro messages
  - `vaults.py`: treasury, shrine (pray `p` for heal + permanent blessing), trap room, library
  - `traps.py`: 5 trap kinds, passive detection, search (`S`), confirm before stepping on known traps
  - New monsters: myconid (confusing spores), magma hound (fire pack)
- Phase 4 leftover done: sleeping monsters, noise from actions, wake chances, sneak attacks
- HUD: theme name, level/XP bar, torch bar, hunger; sleeping tag; text mode shows the same and gets
  `f` search, `p` pray, `+v/+m/+g` level-ups
- Tests: 86 → 132 (new `tests/test_progression.py`); 60-game random bot fuzz across all themes, no crashes;
  real pty smoke test; verified from a fresh clone after pushing
- mini/ascii-animations (new): fire, starfield, Game of Life, spinning torus, plasma, digital rain
