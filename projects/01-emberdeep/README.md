# 🔥 Emberdeep

A dependency-free terminal roguelike written in pure Python. Descend through
procedurally generated, ever-hotter caverns, fight monsters, gather loot and
try to reach the Ember Heart at depth 10 — slay its guardian and carry the Heart away.

**Status:** in development — fully playable and winnable (built hourly, see [ROADMAP.md](ROADMAP.md))

## Run
```bash
cd projects/01-emberdeep
python -m emberdeep          # random seed (resumes your saved game if there is one)
python -m emberdeep 1234     # fixed seed
python -m emberdeep --daily  # today's shared daily dungeon (--daily=2026-11-07 replays a day)
python -m emberdeep --new    # ignore the saved game
python -m emberdeep --scores # print the hall of fame
python -m emberdeep --explore  # practice run: save survives loading, wizard powers, unranked
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
| arrows · `hjkl yubn` · numpad | move / attack (bump a closed door to open it) |
| `.` `5` `s` | wait |
| `g` `,` | pick up |
| `i` + letter | use an item (scrolls may open the targeting cursor; eat food, light torches) |
| `d` + letter | drop |
| `w` + letter | equip / remove |
| `t` + letter | throw an item at a target (potions shatter, daggers fly true) |
| `>` | descend stairs |
| `x` `;` | look around (`Tab` cycles creatures and items) |
| `m` | message history (scroll with `j`/`k`, PgUp/PgDn) |
| `S` | search for hidden traps (radius 2) |
| `p` | pray at an altar (once each) |
| `c` | close an adjacent door (asks for a direction if there are several) |
| `H` | hall of fame |
| `T` | run timeline (depth chart + notable events) |
| `W` | wizard powers (explore mode only) |
| `?` | help · `Q` save & quit |

Targeting: move the cursor, `Tab` jumps between enemies, `Enter`/`f` fires, `Esc` cancels.
When you level up a popup asks for your boon (`v` / `m` / `g`).

## Controls (text mode)
Type keys then Enter (chainable, e.g. `ddddw`): `w a s d` move · `q e z c` diagonals ·
`.` wait · `g` pick up · `i` inventory · `u<letter>` use/equip · `r<letter>` drop ·
`>` descend · `f` search · `p` pray · `k` close door · `t<letter>` throw at the nearest enemy ·
`+v`/`+m`/`+g` level-up boon · `T` timeline · `W<letter>` wizard power (explore mode) · `x` save & quit
(statuses appear in brackets on the status line)

## Items
| Glyph | Items |
|---|---|
| `!` | potions of healing / greater healing (cure poison), speed, liquid fire, venom |
| `?` | scrolls of lightning (auto-targets), fireball (area), confusion, teleportation |
| `/` | dagger (great for throwing), sword, war axe, warhammer (knocks foes back) |
| `[` | leather armor, chain mail, ember plate |
| `=` | rings of strength, protection, vitality |
| `(` | torch (refuels your light) |
| `%` | food ration, glowcap mushroom (fungal caves) |
| `-` | iron key (opens one locked door) |
| `*` | the Ember Heart — the goal of the game |

Loot gets better with depth (see `loot.py`) and each theme favours some items.

**Weight & pack space:** every item weighs something (rings nothing, ember plate 20). You can
carry 40 + 4 × your *base* power (Might boons and shrine blessings raise it) without trouble;
above that you are **burdened** and move at ¾ speed, and past 1.5× you can't pick anything
else up. The sidebar shows `Load` and `Pack` (26 letter slots); you're warned as the last
slots fill up. The inventory lists each item's weight.

**Unidentified items:** every run shuffles appearances onto potions and scrolls — a
"murky potion", a 'scroll labelled "ZUNVEX"'. Only healing potions are known from the start.
Using (or throwing) one identifies the whole kind. Unknown scrolls go off at the nearest
enemy — or at you, if nobody's around: reading an unknown confusion scroll alone confuses
you, an unknown fireball explodes on the spot. The morgue file lists your discoveries.

**Throwing** (`t`): the item flies along the targeting line and stops at the first creature.
Potions shatter — *liquid fire* bursts into flame (radius 1), *venom* poisons everything it
splashes, healing and speed potions affect whatever they hit. Weapons deal damage and land at
the target's feet (daggers get +3).

## Monsters
| Glyph | Monster | Behaviour |
|---|---|---|
| `r` | rat | chases |
| `k` | kobold | **coward**, **scavenger** — flees when hurt, recovers out of sight; picks up loot, drinks healing potions |
| `j` | jackal | **pack**, fast (150) — howls, lurks until the pack gathers, then rushes |
| `i` | ember imp | **caster** — ember bolt (damage + may set you on fire), keeps its distance |
| `s` | cave spider | fast (120), poisonous bite |
| `k` | kobold shaman | **caster**, **scavenger** — hex of slowness |
| `b` | fire beetle | slow (70), armoured, burning bite |
| `m` | myconid | slow (80), spores may confuse you (fungal caves) |
| `h` | magma hound | **pack**, fast (140), burning bite (magma halls) |
| `T` | cave troll | chases, hits hard, can knock you back (into lava's edge!) |
| `&` | **Ember Guardian** | the final boss (depth 10) — see below |

**Scavengers** (kobolds) wander over to items lying around when they have nothing to hunt:
they brandish better weapons (+power), stash healing potions to drink later and fill a sack
with anything else — all of which spills onto the floor when they die. Keys and the Ember
Heart are left alone.

Monsters path with A*, remember where they last saw you and walk there to search.
**Energy system:** every creature gains energy proportional to its speed; it acts each
time it reaches 100, so fast monsters get several moves per turn and slow ones skip turns.
Being hasted or slowed changes how much time your own actions take.

**Stealth:** many monsters start asleep (dimmed on the map, `z` tag in the sidebar).
Every action makes noise (walking 1, fighting 4, fireballs 8); sleepers within earshot or
right next to you may wake. Attacking a sleeping monster is a **sneak attack** (+power damage).

**Status effects:** burning and poisoned deal damage each action, confused creatures
stumble randomly, slowed halves speed, hasted doubles it (haste and slow cancel).
Fire creatures (imps, fire beetles, magma hounds) are immune to burning.

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
| 10 | the Ember Heart | the final arena: no stairs, the guardian's sanctum ringed by lava |

**Special rooms:** treasury (good loot, sleeping guards), shrine (altar `_`: pray once for a
full heal and a permanent blessing), trap room (bait on a trapped floor), library (scrolls).

**Traps** `^`: poison dart, fire, snare (slows), alarm (wakes the level), teleport. They are
hidden until you notice them (when adjacent) or search (`S`). Stepping onto a known trap
needs a second deliberate move. Monsters never trigger traps.

**Locked doors** (red `+`): now and then a room — often a treasury, otherwise a storeroom with
extra loot — is sealed shut. An **iron key** lies somewhere you can reach; bump the door with it
to unlock it. No key? Bump twice to start forcing the door: each try takes a turn, is very
loud, and succeeds more often the mightier you are. Monsters can't open locked doors.

**Braziers** (`*` set into a wall, mostly in the Magma Halls and the Ember Heart): they light up
their surroundings. You can see into a lit area from up to 20 tiles away even with a dying
torch — while creatures standing in the light can't see *you* lurking in the dark.

**Knockback:** warhammer blows can shove a monster back a square. A monster knocked into lava
is consumed (fire creatures climb back out); the Guardian is too heavy to budge.

**Doors:** BSP levels have doors. Closed doors (`+`) block movement and sight — bump into one
to open it (`'`), press `c` to close it again. Monsters open doors when they hunt you, but a
closed door hides you from anything on the other side — handy for breaking line of sight.

## The Ember Guardian
Depth 10 is a hand-shaped arena: a wide molten cavern with basalt pillars for cover and
the guardian's sanctum inside a ring of lava crossed by three narrow bridges. The
**Ember Guardian** (`&`, 150 HP) is immune to fire and confusion and fights in phases:

1. **Awakened** — melee and *magma burst* (ranged, sets you alight).
2. **Kindled** (≤ 66 % HP) — summons magma hounds, fire beetles and imps; *fire nova*
   scorches everything within two tiles.
3. **Enraged** (≤ 33 % HP) — faster (140) and stronger, abilities come more often.

When it dies its servants crumble and it leaves the **Ember Heart** (`*`). Pick it up to win.

## Saves, scores & the daily run
* **Save & quit** with `Q` (curses) or `x` (text mode). Starting the game again resumes the
  run — and deletes the save (**permadeath**: no reloading after a bad fight). Dying or
  winning deletes it too. The save is plain JSON and includes the random generator's state,
  so a resumed game continues exactly as it would have.
* Every finished run is written to a **morgue file** (character, equipment, pack, kills by
  monster, last messages and a map dump) and scored into the **hall of fame**
  (depth × 150 + XP + kills, plus a big victory bonus that is larger for faster wins).
* **Run timeline:** the game records when you reached each depth, levelled up, first slew each
  kind of monster, and how the run ended. `T` shows it any time; after a run, `T` on the end screen opens the
  "story of your run" screen, and it is a section of the morgue file, with an ASCII depth chart.
* **Explore mode** (`--explore`): a practice mode. Loading an explore save does *not* delete it
  (reload after a death), finished runs are recorded unranked as `[explore]`, and `W` opens
  wizard powers: map the level, heal fully, identify everything, jump to the stairs, descend,
  conjure a potion of greater healing. `--explore` with an existing save resumes that save.
* **Daily run** (`--daily`): the seed comes from the UTC date, so everyone gets the same
  dungeon that day. Only your first daily attempt is ranked; repeats are marked practice.
* Files live in `$EMBERDEEP_HOME` (default `~/.emberdeep`): `save.json`, `scores.json`, `morgue/`.

## Balance bot
`python -m emberdeep.bot [runs] [report.md]` lets an automated player play many seeded games
(in parallel) and writes a Markdown balance report. The bot only uses the public game API
and sees what a human would: it explores the nearest frontier, fights, zaps scrolls at tough
foes, drinks potions when low, eats, refuels, wears the best gear, opens locked doors and
finally hunts the Guardian. Its results drove the current tuning — see [BALANCE.md](BALANCE.md).

## Animation
Spells and projectiles are animated in the curses UI: ember bolts and thrown items fly across
the map with a short trail, lightning flashes along its line, fireballs, shattering potions and
the Guardian's fire nova blossom outward ring by ring. The game logic only *records* effects
(`fx.py`); the UI plays them (≈35 ms per frame) and text mode ignores them.

See [SCREENSHOTS.md](SCREENSHOTS.md) for captures of the real UI (made with
`python -m emberdeep.screenshot`).

## Architecture
| Module | Purpose |
|---|---|
| `geometry.py` | Rect, Bresenham lines, distances |
| `tiles.py` / `gamemap.py` | Tile types (incl. open/closed doors) and the map with visibility memory |
| `dungeon.py` | Room-and-corridor generator |
| `gen_bsp.py` / `gen_caves.py` | BSP generator with doors, cellular-automata caves |
| `levelgen.py` / `themes.py` | Theme-driven level assembly, decorations (lava kept connectable) |
| `boss.py` | Boss arena generator and the Ember Guardian's phased AI |
| `save.py` | JSON save/load with RNG state, permadeath helpers, data directory |
| `scores.py` / `morgue.py` / `daily.py` | Hall of fame, morgue files + run finishing, daily seeds |
| `vaults.py` / `traps.py` | Special rooms, shrines & prayer; trap placement, detection, effects |
| `locks.py` / `lighting.py` | Locked rooms + keys + forcing; wall braziers and lit areas |
| `identify.py` / `throwing.py` / `knockback.py` | Unidentified potions & scrolls; throwing; shoves into lava |
| `bot.py` | Automated balance-testing player and report generator |
| `encumbrance.py` | Item weights, carrying capacity, burden & pack-slot warnings |
| `scavenge.py` | Monsters picking up floor items (weapons, potions, sacks) and dropping them on death |
| `timeline.py` | Run events, turns per depth, ASCII depth chart |
| `explore.py` | Explore mode and the wizard commands |
| `fx.py` | Recorded spell/projectile effects and their animation frames |
| `screenshot.py` | In-memory screen + bot to capture ASCII screenshots of the UI |
| `progression.py` / `resources.py` | XP levels & boons; torch fuel and hunger |
| `fov.py` | Recursive shadowcasting field of view |
| `entities.py` | Entities, fighters (with equipment bonuses), monster templates, immunities |
| `items.py` | Item data + templates (potions, scrolls, supplies, weapons, armor, rings) |
| `inventory.py` / `equipment.py` | a–z stacking inventory, weapon/armor/ring slots |
| `loot.py` | Depth-aware loot tables with theme bias |
| `targeting.py` | Projectile paths, blast areas, targeting cursor |
| `combat.py` | Melee resolution (with sneak-attack bonus) |
| `pathfinding.py` | A*, Dijkstra maps, flee (safety) maps |
| `ai.py` | Monster behaviours (chase/coward/caster/pack), spells, sleeping & waking, doors |
| `status.py` | Status effects with ticking, stacking and speed multipliers |
| `look.py` | Look-mode cell descriptions |
| `messages.py` | Colour-aware message log with stacking |
| `game.py` | Turn logic + energy system, levels, item effects, statuses, victory (renderer-independent) |
| `hud.py` / `colors.py` / `keys.py` | Sidebar content, colour table, key bindings |
| `ui_curses.py` | Real-time curses interface (testable through a fake screen) |
| `render_ascii.py` | Text renderer for text mode |

Tests: 271 unit tests, including full UI runs against a fake curses screen and
save/load determinism checks (a loaded game must replay identically to the original).
