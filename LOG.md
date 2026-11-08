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

## 2026-11-07 23:00 UTC — hour 5: Emberdeep endgame — Ember Guardian boss, save/load + permadeath, hall of fame, morgue, daily seed, doors
- Emberdeep Phase 6 complete:
  - `boss.py`: depth 10 is a hand-shaped arena (molten cavern, basalt pillars, lava-ringed sanctum with
    three bridges, no stairs). The **Ember Guardian** fights in 3 phases: magma burst, summoned fire
    creatures, fire nova, enrage (speed 140, +2 power). Killing it drops the Ember Heart; picking it up wins
  - Victory state (`game.victory`, victory screen), fire immunity for fire creatures, boss immune to
    burning and confusion, kill counts per monster
  - `save.py`: full JSON save/load including the RNG state (a loaded game replays identically — tested),
    atomic writes, corrupt/old-save detection, permadeath (save consumed on load, deleted on death/victory)
  - `scores.py`: hall of fame (top 50, `H` in game, `--scores`), score formula with victory/speed bonus
  - `morgue.py`: morgue file per finished run (character, boons, gear, pack, kills, last messages, map dump)
    and `finish_run()` used by both front-ends
  - `daily.py`: `--daily` / `--daily=YYYY-MM-DD` seed from the UTC date; repeat daily attempts are unranked
  - CLI rewritten: resume save automatically, `--new`, `--scores`, `--daily`, unknown-argument help
- Phase 5 leftover: doors open/close — closed doors block movement and sight, bump to open, `c` to close
  (`k` in text mode), monsters open doors while hunting, BSP levels get a mix of open and closed doors
- Tests: 132 → 173 (new `tests/test_endgame.py`, `tests/test_save.py`); 40-game random bot fuzz with save
  round-trips; 12 scripted boss fights (strong hero wins 9/12); real pty smoke test of save → resume;
  verified from a fresh clone after pushing
- mini/drawings: Koch snowflake, dragon curve, Hilbert curve, ASCII mountains, Lissajous figures, Julia sets

## 2026-11-08 00:00 UTC — hour 6: Emberdeep polish — unidentified items, throwing, locked doors, braziers, knockback, balance bot
- Emberdeep Phase 3–5 leftovers done:
  - `identify.py`: per-run appearances for every potion and scroll ("murky potion", 'scroll labelled "ZUNVEX"');
    healing is known from the start; using/throwing identifies the whole kind; blind reads are risky
    (unknown confusion with no foe confuses you, unknown fireball goes off on the spot); morgue lists discoveries
  - `throwing.py` + `t` key (curses and text mode): projectiles stop at the first creature; potions shatter
    (new **liquid fire** burst and **venom** splash potions, healing/speed affect the target); daggers +3 thrown
  - `locks.py`: locked rooms (treasury or loot-filled storeroom) behind red `+` doors that keep the level
    connected; an iron key is always placed reachable; or force the door (loud, chance grows with power)
  - `lighting.py` + FOV: wall braziers light their surroundings; lit cells are visible from 20 tiles away
    even with a dying torch, and monsters standing in the light can't see you lurking in the dark
  - `knockback.py`: new **warhammer** shoves foes back — into lava to their doom (fire creatures climb out,
    the boss is immovable); cave trolls can hurl you to the lava's edge
  - Kobolds may carry a healing potion, drink it when hurt and drop it when killed
  - Tiles get separate save codes (locked doors share the `+` glyph); saves store identification state,
    old saves load with everything identified
- Phase 7: `bot.py` balance bot (explores frontiers with cached BFS, fights, zaps, drinks, eats, unlocks or
  forces doors, hunts the Guardian; parallel `run_many`, Markdown `report`). First tuning pass from its data
  (5% → 53% bot wins over 200 seeds): imps kite less and burn less, fewer monster groups, steeper XP curve,
  Ember Guardian 150 HP / 9 power, fewer healing potions — written up in `BALANCE.md`
- Tests: 173 → 224 (new `tests/test_features.py`); real pty curses smoke test; text-mode smoke test
- mini/puzzles: Lights Out (GF(2) elimination), Mastermind (Knuth minimax), peg solitaire (symmetry-pruned
  DFS), cryptarithm solver, magic squares of any order, water jugs (BFS)
