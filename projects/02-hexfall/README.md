# ⬡ Hexfall

A turn-based **hex-grid tactics game** for the browser, in plain JavaScript ES modules —
no build step, no dependencies. Two armies deploy on a procedurally generated battlefield
of plains, forests, hills, rivers and villages; capture villages for income, use terrain
for cover, and outmanoeuvre an AI opponent.

**Status:** 🚧 Phases 1–3 ✅ — a complete **hot-seat battle** runs in the browser: two armies of six
unit types deploy, move under zones of control, fight with terrain, flanking, line of sight and
counter-attacks, gain veteran perks, heal in villages, and save/load. Next: Phase 4 (economy &
objectives) and Phase 5 (AI opponent). Built hourly, see [ROADMAP.md](ROADMAP.md).

## Run
```bash
cd projects/02-hexfall
python3 -m http.server 8000     # any static server works (ES modules need http://, not file://)
# open http://localhost:8000/#7  (the part after # is the map seed; text seeds work too)
npm test                        # or: node --test tests/*.test.js   (Node 18+)
```

**How to play (hot-seat):** Red moves first. Click one of your units: yellow hexes show where it
can go, red rings mark enemies it can attack this turn. Click a yellow hex to move (you can keep
moving while move points last), or click a ringed enemy to attack — melee units step next to the
target by themselves, choosing the best hex. Hover an enemy to see the exact damage forecast.
Press **E** to end the turn, **U** to undo a move, **N**/**Tab** for the next ready unit, **Esc**
to deselect. The mouse wheel zooms, dragging pans, the minimap jumps. The battle autosaves; Save/Load
use a browser slot, Export/Import a JSON file. Rout the enemy army to win.

## Units
| Unit | HP | Melee | Ranged (range) | Armour | MP | Cost | Special | Veteran perk |
|---|---|---|---|---|---|---|---|---|
| Spearman | 34 | 9 | — | 2 | 5 | 14 | ×1.5 damage to mounted units | Phalanx: +2 armour |
| Swordsman | 40 | 11 | — | 3 | 5 | 17 | | Blademaster: +3 melee |
| Archer | 28 | 4 | 8 (3) | 1 | 5 | 15 | needs line of sight | Longshot: +1 range |
| Cavalry | 38 | 10 | — | 2 | 8 | 20 | mounted: forest/swamp +1 MP | Outrider: +1 MP |
| Mage | 24 | 3 | 11 (2) | 0 | 5 | 20 | magic ignores terrain defence | Arcanist: +3 ranged |
| Healer | 26 | 4 | — | 1 | 5 | 16 | heals adjacent allies 4/turn | Medic: heals 8 |

## Combat rules
- **Damage** of one strike = attack × flanking × (1 − target terrain defence) × anti-cavalry × roll − armour,
  rounded, at least 1. The roll is one of 0.8 / 0.9 / 1.0 / 1.1 / 1.2, drawn from the game's seeded RNG.
- **Counter-attack:** if the defender survives and has the same kind of attack that reaches the
  attacker (melee next to it, or ranged within its range and line of sight), it strikes back once.
- **Flanking:** +10% melee damage for every *other* friendly unit next to the target (max +30%).
- **Line of sight:** forests and villages block shots unless the shooter stands higher (hills);
  mountains always block. Lines along hex edges count as clear if either side is clear.
  **High ground** (hills) gives ranged units +1 range.
- **Zone of control:** a unit that steps next to an enemy stops there. Friends can be passed through.
- **Experience:** 1 XP × enemy level for every exchange survived, 8 × enemy level for a kill.
  20 XP → **Veteran** (type perk), 45 more → **Elite** (+1 attack, +1 armour); each promotion adds
  15% HP and heals fully.
- **Healing** at the start of your turn: +8 in a village, +4 next to a healer (the best one applies).
- The **forecast** tooltip enumerates all 25 roll combinations exactly (a dead target never
  counters), giving damage ranges, kill chance and your risk of dying.

## How the map is made
1. **Noise:** two fractal value-noise fields (elevation and moisture) are sampled at each
   hex's pixel centre, so features look natural on the hex lattice.
2. **Terrain:** elevation picks water → shallows → sand/swamp → plains/forest → hills →
   mountains; moisture turns dry land into forest or swamp (`classify` in `mapgen.js`).
3. **Playability:** the largest connected passable region must cover ≥ 45% of the map;
   both deployment zones are taken from it, at opposite ends — otherwise the generator
   retries with a forked seed (deterministic: same seed ⇒ same map).
4. **Rivers** spring from the highest hills and run downhill to the sea (pooling into
   shallows when trapped in a hollow).
5. **Villages** are scattered over the main region (≥ 4 hexes apart, away from spawns), and
   **roads** link the two camps through the villages with A* that prefers easy ground and
   existing roads (½ MP per road hex); where a road meets a river it builds a **bridge**.
6. **Symmetric mode** (`symmetric: true`, the *Symmetric* checkbox) point-mirrors the map
   through its centre — terrain, deployment zones and villages — for perfectly fair battles.

## Terrain
| Terrain | Move cost | Defence | Notes |
|---|---|---|---|
| Road | ½ | 0% | laid by the generator between camps and villages |
| Plains | 1 | 0% | |
| Village | 1 | 30% | capturable, blocks sight |
| Forest | 2 | 25% | blocks sight |
| Hills | 2 | 20% | high ground |
| Sand | 2 | 0% | |
| Bridge | 1 | 0% | where roads cross rivers |
| Swamp / Shallows / River | 3 | −10% | fighting knee-deep is a bad idea |
| Water / Mountain | — | — | impassable (mountains block sight) |

A unit with its full move points can always take one step onto passable ground, even if
the step costs more than it has.

## Code
| File | Purpose |
|---|---|
| `src/hex.js` | Axial/cube hex math: neighbours, distance, lines, rings, spirals, rotation, pixel & offset conversion |
| `src/rng.js` | Seeded mulberry32 RNG (ints, picks, shuffles, weighted choice, forks) + FNV-1a string seeds |
| `src/noise.js` | 2D value noise with fractal octaves |
| `src/terrain.js` | Terrain table (costs, defence, sight, colours) |
| `src/map.js` | `HexMap` (odd-r rectangle of tiles), JSON round trip, ASCII dump |
| `src/pathfind.js` | Binary heap, Dijkstra reachable area, path reconstruction, A*, flood fill |
| `src/mapgen.js` | Procedural battlefield generator (terrain, rivers, connectivity, spawns, villages, roads + bridges, symmetry) |
| `src/render.js` | Canvas renderer: shaded hexes, terrain decorations, zones, reach + path overlays |
| `src/camera.js` | Zoom-at-cursor, clamped panning, visible rectangle + centring for the minimap |
| `src/units.js` | Unit types, perks, unit records, derived stats, XP and promotions |
| `src/movement.js` | Unit movement area: mounted terrain costs, unit blocking, zones of control, routes |
| `src/sight.js` | Line of sight (height-aware blockers, edge-tie handling) and visible sets |
| `src/combat.js` | Attack kinds, damage modifiers, exact forecasts, seeded resolution with counters and XP |
| `src/game.js` | `Game`: deployment, turns, move/undo, attack plans, healing upkeep, victory, JSON |
| `src/save.js` | Save text, storage slots (localStorage or the in-memory `MemoryStorage`) |
| `src/animate.js` | Pure tweening: eased moves along routes, attack lunges |
| `src/main.js` | Browser UI: battle controls, roster, log, forecast tooltip, animations, keys, saves, camera, minimap |

Tests (`node --test`, 67): hex math properties, camera maths, RNG/noise determinism, heap
order, A* optimality, downhill rivers, point symmetry, 25 generated maps checked for
determinism and playability; unit stats and promotions; movement with ZOC, blocking and mounted
costs; damage rules, flanking, line of sight (incl. symmetry over thousands of pairs), exact
forecasts vs. hand-computed odds, seeded attack resolution; turns, undo, healing, victory, save
round trips where a loaded game replays identically; animation tweening.

`tests/browser-smoke.mjs` drives the real page in Chromium (Playwright): it selects, moves, undoes,
then plays a whole battle with mouse clicks and keys, saves and loads, and fails on any page error.
