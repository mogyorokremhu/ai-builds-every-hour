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
- [ ] Throwing items / potions shatter on impact
- [ ] Unidentified potions & scrolls with random names per run
- [ ] Item weight/encumbrance or pack limit warnings

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
- [ ] Spell projectiles animated in the curses UI
- [ ] Monsters pick up / use items (kobolds drink potions)

## Phase 5 — Progression ✅ (core)
- [x] XP levels with stat choice on level-up (Vitality / Might / Guard + auto HP)
- [x] Hunger/torch fuel resource (torch shrinks FOV, starvation damage, rations/glowcaps/torches)
- [x] Unique depth themes (cellars, fungal caves, magma halls, ember heart) with colours, decor, fauna bias
- [x] Alternative generators: cellular-automata caves, BSP (with doors)
- [x] Vaults and special rooms (treasury, shrine, trap room, library)
- [x] Traps (hidden, passive detection, search command, 5 kinds, confirm before stepping on known ones)
- [x] New monsters: myconid (confusing spores), magma hound (fire pack)
- [ ] Openable/closable doors (and the occasional locked one)
- [ ] Lit rooms / wall braziers that don't need your torch
- [ ] Knockback into lava (and monsters avoiding lava when fleeing)

## Phase 6 — Endgame & persistence
- [ ] Boss at depth 10: the Ember Heart guardian
- [ ] Save/load (JSON) + permadeath delete on death
- [ ] High-score table and morgue file (run summary)
- [ ] Daily seed mode

## Phase 7 — Polish
- [ ] Balance pass with an automated bot that plays 1000 runs and reports stats
- [ ] Full docs + gameplay GIF/ASCII screenshots
- [ ] Final cleanup, type-check, 80%+ test coverage
