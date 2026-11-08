# Emberdeep Roadmap

Target: ~2–3 days of hourly work. Each run should tick off several items.

## Phase 1 — Core engine
- [x] Geometry helpers (Rect, Bresenham, Chebyshev)
- [x] Tile + map model with visible/explored memory
- [x] Room-and-corridor dungeon generator (seeded, deterministic)
- [x] Shadowcasting FOV
- [x] Player + monster entities, monster templates by depth
- [x] Melee combat + message log with stacking
- [x] Turn loop, stairs, multiple depths
- [x] ASCII renderer + playable text-mode entry point
- [x] Unit tests for core systems

## Phase 2 — Real-time interface ✅
- [x] curses UI with instant key input (fallback to text mode on Windows without curses)
- [x] Colors per tile/entity, dim colors for remembered tiles
- [x] Sidebar: HP bar, stats, visible monsters list
- [x] Message log panel with scrollback screen
- [x] Help screen (`?`)
- [x] Scrolling camera so the map fits small terminals
- [x] Fake-screen test harness that drives the whole UI with scripted keys

## Phase 3 — Items & inventory ✅
- [x] Item entity type + pickup (`g`) and drop
- [x] Inventory screen with letters a–z
- [x] Healing potions, scrolls (lightning, fireball, confusion, teleport)
- [x] Targeting mode for ranged scrolls (cursor + Bresenham line)
- [x] Equipment slots: weapon, armor, ring; equip/unequip
- [x] Loot tables by depth
- [x] Look mode (`x`): move a cursor and describe what's there
- [x] Throwing items (`t`) / potions shatter on impact (liquid fire, venom, healing, speed)
- [x] Unidentified potions & scrolls with random names per run (risky blind reads, morgue discoveries)
- [x] Item weight/encumbrance (burdened = ¾ speed, hard limit at 1.5×, capacity grows with Might) + pack-slot warnings

## Phase 4 — Smarter monsters ✅ (core)
- [x] A* pathfinding (stdlib heapq) + Dijkstra maps and Brogue-style flee maps
- [x] Monsters remember the player's last seen position
- [x] AI kinds: chase, coward (flees at low HP), ranged caster, pack hunter
- [x] Status effects system: burning, poisoned, confused, slowed (+ hasted)
- [x] Energy/speed system (fast & slow monsters)
- [x] New monsters: jackal packs, cave spider (poison), fire beetle (burns), kobold shaman (slow hex)
- [x] Monster on-hit statuses, spells with cooldowns and line-of-fire checks
- [x] Potion of speed; healing cures poison; death cause tracked
- [x] Sleeping monsters + noise/stealth (monsters wake when you're loud or close; sneak attacks)
- [x] Spell projectiles animated in the curses UI (bolts with trails, lightning beams, ring-by-ring blasts; `fx.py`)
- [x] Monsters use items: kobolds may carry a healing potion, drink it when hurt, drop it on death
- [x] Monsters pick up items lying on the floor (kobold scavengers: brandish weapons, stash potions, sacks spill on death)

## Phase 5 — Progression ✅ (core)
- [x] XP levels with stat choice on level-up (Vitality / Might / Guard + auto HP)
- [x] Hunger/torch fuel resource (torch shrinks FOV, starvation damage, rations/glowcaps/torches)
- [x] Unique depth themes (cellars, fungal caves, magma halls, ember heart) with colours, decor, fauna bias
- [x] Alternative generators: cellular-automata caves, BSP (with doors)
- [x] Vaults and special rooms (treasury, shrine, trap room, library)
- [x] Traps (hidden, passive detection, search command, 5 kinds, confirm before stepping on known ones)
- [x] New monsters: myconid (confusing spores), magma hound (fire pack)
- [x] Openable/closable doors (bump to open, `c` to close; monsters open them; closed doors block sight)
- [x] The occasional locked door (iron key always reachable, or force it: loud, power-based)
- [x] Lit rooms / wall braziers that don't need your torch (see lit areas from afar; stay hidden in the dark)
- [x] Knockback into lava (warhammer; trolls shove you; fire creatures climb out; lava is never walkable so fleeing monsters avoid it)

## Phase 6 — Endgame & persistence ✅
- [x] Boss at depth 10: the Ember Guardian in a lava-ringed arena (3 phases: magma burst, summons, fire nova, enrage)
- [x] Victory: the guardian drops the Ember Heart; picking it up wins the run
- [x] Fire immunity for fire creatures; boss immune to burning & confusion
- [x] Save/load (JSON, includes RNG state so a loaded game continues identically) + permadeath
      (save consumed on load, deleted on death/victory)
- [x] High-score table (hall of fame, `H` in game, `--scores` on the CLI) and morgue file (run summary + map dump)
- [x] Daily seed mode (`--daily`, `--daily=YYYY-MM-DD`; repeat attempts marked practice)
- [x] Post-run "story of your run" screen with a timeline + ASCII depth chart (`T` any time; also in the morgue)
- [x] `--explore` mode: save kept on load, unranked `[explore]` scores, wizard powers (`W`: map, heal, identify, stairs, descend, conjure)

## Phase 7 — Polish
- [x] New items: potions of liquid fire & venom, warhammer, iron keys; dagger throw bonus
- [x] Balance bot (`python -m emberdeep.bot N report.md`, parallel) + first balance pass from a 200-run report (BALANCE.md)
- [x] Full 1000-run sweep after the remaining features land: 27.0% bot wins, inside the 25–40% band (BALANCE.md)
- [x] Docs for every system + ASCII screenshots of the real UI (`python -m emberdeep.screenshot` → SCREENSHOTS.md)
- [x] 80%+ test coverage (95% line coverage with `coverage.py`; new CLI/text-mode tests)
- [ ] Type-check clean under mypy (167 Optional-access warnings: add typed player accessors)
- [ ] Final cleanup pass (dead code, docstrings) and finishing touches
