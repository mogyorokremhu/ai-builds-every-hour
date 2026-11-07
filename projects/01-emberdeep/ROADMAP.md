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
- [ ] Look mode (`x`): move a cursor and describe what's there
- [ ] Throwing items / potions shatter on impact
- [ ] Unidentified potions & scrolls with random names per run
- [ ] Item weight/encumbrance or pack limit warnings

## Phase 4 — Smarter monsters
- [ ] A* pathfinding (stdlib heapq)
- [ ] Monsters remember the player's last seen position
- [ ] AI kinds: chase, coward (flees at low HP), ranged caster, pack hunter
- [ ] Status effects system: burning, poisoned, confused, slowed
- [ ] Energy/speed system (fast & slow monsters)

## Phase 5 — Progression
- [ ] XP levels with stat choice on level-up
- [ ] Hunger/torch fuel resource
- [ ] Unique depth themes (cellars, fungal caves, magma halls)
- [ ] Alternative generators: cellular-automata caves, BSP
- [ ] Vaults and special rooms (treasury, shrine, trap room)
- [ ] Traps (hidden, detectable)

## Phase 6 — Endgame & persistence
- [ ] Boss at depth 10: the Ember Heart guardian
- [ ] Save/load (JSON) + permadeath delete on death
- [ ] High-score table and morgue file (run summary)
- [ ] Daily seed mode

## Phase 7 — Polish
- [ ] Balance pass with an automated bot that plays 1000 runs and reports stats
- [ ] Full docs + gameplay GIF/ASCII screenshots
- [ ] Final cleanup, type-check, 80%+ test coverage
