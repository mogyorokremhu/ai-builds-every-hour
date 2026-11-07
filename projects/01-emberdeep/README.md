# 🔥 Emberdeep

A dependency-free terminal roguelike written in pure Python. Descend through
procedurally generated, ever-hotter caverns, fight monsters, gather loot and
try to reach the Ember Heart at depth 10.

**Status:** in development (built hourly, see [ROADMAP.md](ROADMAP.md))

## Run
```bash
cd projects/01-emberdeep
python -m emberdeep          # random seed
python -m emberdeep 1234     # fixed seed
python -m unittest discover -s tests -t .   # tests
```

## Interface
On Linux/macOS the game opens a real-time **curses** interface: a scrolling coloured map,
a sidebar (HP bar, level/XP, torch, food, equipment, monsters in view) and a message log.
On platforms without curses (or with `--text`) it falls back to the line-based text mode.

```bash
python -m emberdeep --text   # force text mode
```

## Controls (curses)
| Key | Action |
|---|---|
| arrows · `hjkl yubn` · numpad | move / attack |
| `.` `5` `s` | wait |
| `g` `,` | pick up |
| `i` + letter | use an item (scrolls may open the targeting cursor; eat food, light torches) |
| `d` + letter | drop |
| `w` + letter | equip / remove |
| `>` | descend stairs |
| `x` `;` | look around (`Tab` cycles creatures and items) |
| `m` | message history (scroll with `j`/`k`, PgUp/PgDn) |
| `S` | search for hidden traps (radius 2) |
| `p` | pray at an altar (once each) |
| `?` | help · `Q` quit |

Targeting: move the cursor, `Tab` jumps between enemies, `Enter`/`f` fires, `Esc` cancels.
When you level up a popup asks for your boon (`v` / `m` / `g`).

## Controls (text mode)
Type keys then Enter (chainable, e.g. `ddddw`): `w a s d` move · `q e z c` diagonals ·
`.` wait · `g` pick up · `i` inventory · `u<letter>` use/equip · `r<letter>` drop ·
`>` descend · `f` search · `p` pray · `+v`/`+m`/`+g` level-up boon · `x` quit
(statuses appear in brackets on the status line)

## Items
| Glyph | Items |
|---|---|
| `!` | potions of healing / greater healing (cure poison), potion of speed |
| `?` | scrolls of lightning (auto-targets), fireball (area), confusion, teleportation |
| `/` | dagger, sword, war axe |
| `[` | leather armor, chain mail, ember plate |
| `=` | rings of strength, protection, vitality |
| `(` | torch (refuels your light) |
| `%` | food ration, glowcap mushroom (fungal caves) |

Loot gets better with depth (see `loot.py`) and each theme favours some items.

## Monsters
| Glyph | Monster | Behaviour |
|---|---|---|
| `r` | rat | chases |
| `k` | kobold | **coward** — flees along a safety map when hurt, recovers out of sight |
| `j` | jackal | **pack**, fast (150) — howls, lurks until the pack gathers, then rushes |
| `i` | ember imp | **caster** — ember bolt (damage + may set you on fire), keeps its distance |
| `s` | cave spider | fast (120), poisonous bite |
| `k` | kobold shaman | **caster** — hex of slowness |
| `b` | fire beetle | slow (70), armoured, burning bite |
| `m` | myconid | slow (80), spores may confuse you (fungal caves) |
| `h` | magma hound | **pack**, fast (140), burning bite (magma halls) |
| `T` | cave troll | chases, hits hard |

Monsters path with A*, remember where they last saw you and walk there to search.
**Energy system:** every creature gains energy proportional to its speed; it acts each
time it reaches 100, so fast monsters get several moves per turn and slow ones skip turns.
Being hasted or slowed changes how much time your own actions take.

**Stealth:** many monsters start asleep (dimmed on the map, `z` tag in the sidebar).
Every action makes noise (walking 1, fighting 4, fireballs 8); sleepers within earshot or
right next to you may wake. Attacking a sleeping monster is a **sneak attack** (+power damage).

**Status effects:** burning and poisoned deal damage each action, confused creatures
stumble randomly, slowed halves speed, hasted doubles it (haste and slow cancel).

## Progression & survival
* **Levels:** XP from kills fills a level bar. Each level-up asks you to pick a boon —
  **Vitality** (+8 max HP, full heal), **Might** (+1 power) or **Guard** (+1 defense) — and
  always adds +2 max HP.
* **Torch:** your light burns down every turn; the field of view shrinks from 8 to 2 tiles
  as it fades. Light a new torch `(` from your pack.
* **Hunger:** you get hungry over time. Hungry characters stop regenerating; starving ones
  take damage. Eat rations or glowcap mushrooms.

## The depths
| Depths | Theme | Levels |
|---|---|---|
| 1–3 | the Old Cellars | rooms & corridors or BSP halls with doors, rubble; rats & kobolds |
| 4–6 | the Fungal Caves | cellular-automata caves with glowing fungus; spiders & myconids |
| 7–9 | the Magma Halls | BSP halls broken by lava pools (never cutting the level apart); fire beasts |
| 10+ | the Ember Heart | a molten cavern |

**Special rooms:** treasury (good loot, sleeping guards), shrine (altar `_`: pray once for a
full heal and a permanent blessing), trap room (bait on a trapped floor), library (scrolls).

**Traps** `^`: poison dart, fire, snare (slows), alarm (wakes the level), teleport. They are
hidden until you notice them (when adjacent) or search (`S`). Stepping onto a known trap
needs a second deliberate move. Monsters never trigger traps.

## Architecture
| Module | Purpose |
|---|---|
| `geometry.py` | Rect, Bresenham lines, distances |
| `tiles.py` / `gamemap.py` | Tile types and the map with visibility memory |
| `dungeon.py` | Room-and-corridor generator |
| `gen_bsp.py` / `gen_caves.py` | BSP generator with doors, cellular-automata caves |
| `levelgen.py` / `themes.py` | Theme-driven level assembly, decorations (lava kept connectable) |
| `vaults.py` / `traps.py` | Special rooms, shrines & prayer; trap placement, detection, effects |
| `progression.py` / `resources.py` | XP levels & boons; torch fuel and hunger |
| `fov.py` | Recursive shadowcasting field of view |
| `entities.py` | Entities, fighters (with equipment bonuses), monster templates |
| `items.py` | Item data + templates (potions, scrolls, supplies, weapons, armor, rings) |
| `inventory.py` / `equipment.py` | a–z stacking inventory, weapon/armor/ring slots |
| `loot.py` | Depth-aware loot tables with theme bias |
| `targeting.py` | Projectile paths, blast areas, targeting cursor |
| `combat.py` | Melee resolution (with sneak-attack bonus) |
| `pathfinding.py` | A*, Dijkstra maps, flee (safety) maps |
| `ai.py` | Monster behaviours (chase/coward/caster/pack), spells, sleeping & waking |
| `status.py` | Status effects with ticking, stacking and speed multipliers |
| `look.py` | Look-mode cell descriptions |
| `messages.py` | Colour-aware message log with stacking |
| `game.py` | Turn logic + energy system, levels, item effects, statuses (renderer-independent) |
| `hud.py` / `colors.py` / `keys.py` | Sidebar content, colour table, key bindings |
| `ui_curses.py` | Real-time curses interface (testable through a fake screen) |
| `render_ascii.py` | Text renderer for text mode |

Tests: 132 unit tests, including full UI runs against a fake curses screen.
