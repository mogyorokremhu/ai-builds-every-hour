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
a sidebar (HP bar, stats, equipment, monsters in view) and a message log. On platforms
without curses (or with `--text`) it falls back to the line-based text mode.

```bash
python -m emberdeep --text   # force text mode
```

## Controls (curses)
| Key | Action |
|---|---|
| arrows · `hjkl yubn` · numpad | move / attack |
| `.` `5` `s` | wait |
| `g` `,` | pick up |
| `i` + letter | use an item (scrolls may open the targeting cursor) |
| `d` + letter | drop |
| `w` + letter | equip / remove |
| `>` | descend stairs |
| `x` `;` | look around (`Tab` cycles creatures and items) |
| `m` | message history (scroll with `j`/`k`, PgUp/PgDn) |
| `?` | help · `Q` quit |

Targeting: move the cursor, `Tab` jumps between enemies, `Enter`/`f` fires, `Esc` cancels.

## Controls (text mode)
Type keys then Enter (chainable, e.g. `ddddw`): `w a s d` move · `q e z c` diagonals ·
`.` wait · `g` pick up · `i` inventory · `u<letter>` use/equip · `r<letter>` drop ·
`>` descend · `x` quit (statuses appear in brackets on the status line)

## Items
| Glyph | Items |
|---|---|
| `!` | potions of healing / greater healing (cure poison), potion of speed |
| `?` | scrolls of lightning (auto-targets), fireball (area), confusion, teleportation |
| `/` | dagger, sword, war axe |
| `[` | leather armor, chain mail, ember plate |
| `=` | rings of strength, protection, vitality |

Loot gets better with depth (see `loot.py`).

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
| `T` | cave troll | chases, hits hard |

Monsters path with A*, remember where they last saw you and walk there to search.
**Energy system:** every creature gains energy proportional to its speed; it acts each
time it reaches 100, so fast monsters get several moves per turn and slow ones skip turns.
Being hasted or slowed changes how much time your own actions take.

**Status effects:** burning and poisoned deal damage each action, confused creatures
stumble randomly, slowed halves speed, hasted doubles it (haste and slow cancel).

## Architecture
| Module | Purpose |
|---|---|
| `geometry.py` | Rect, Bresenham lines, distances |
| `tiles.py` / `gamemap.py` | Tile types and the map with visibility memory |
| `dungeon.py` | Room-and-corridor generator |
| `fov.py` | Recursive shadowcasting field of view |
| `entities.py` | Entities, fighters (with equipment bonuses), monster templates |
| `items.py` | Item data + templates (potions, scrolls, weapons, armor, rings) |
| `inventory.py` / `equipment.py` | a–z stacking inventory, weapon/armor/ring slots |
| `loot.py` | Depth-aware loot tables |
| `targeting.py` | Projectile paths, blast areas, targeting cursor |
| `combat.py` | Melee resolution |
| `pathfinding.py` | A*, Dijkstra maps, flee (safety) maps |
| `ai.py` | Monster behaviours (chase/coward/caster/pack), spells |
| `status.py` | Status effects with ticking, stacking and speed multipliers |
| `look.py` | Look-mode cell descriptions |
| `messages.py` | Colour-aware message log with stacking |
| `game.py` | Turn logic + energy system, levels, item effects, statuses (renderer-independent) |
| `hud.py` / `colors.py` / `keys.py` | Sidebar content, colour table, key bindings |
| `ui_curses.py` | Real-time curses interface (testable through a fake screen) |
| `render_ascii.py` | Text renderer for text mode |

Tests: 86 unit tests, including full UI runs against a fake curses screen.
