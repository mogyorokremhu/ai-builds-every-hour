# ⬡ Hexfall

A turn-based **hex-grid tactics game** for the browser, in plain JavaScript ES modules —
no build step, no dependencies. Two armies deploy on a procedurally generated battlefield
of plains, forests, hills, rivers and villages; capture villages for income, use terrain
for cover, and outmanoeuvre an AI opponent.

**Status:** 🚧 Phase 1 (map engine) ✅ done — the map generator, movement preview, zoom/pan
and minimap run in the browser today; next comes Phase 2 (units & turns). Built hourly, see [ROADMAP.md](ROADMAP.md).

## Run
```bash
cd projects/02-hexfall
python3 -m http.server 8000     # any static server works (ES modules need http://, not file://)
# open http://localhost:8000/#7  (the part after # is the map seed; text seeds work too)
npm test                        # or: node --test tests/*.test.js   (Node 18+)
```

In the map preview, click a hex to see where a unit with the chosen move points could go;
hover to see the cheapest path and terrain details. The mouse wheel zooms around the cursor,
dragging pans, and the minimap (bottom right) shows where you are — click it to jump.

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
| `src/main.js` | Browser entry: seed controls, hover info, click-to-preview movement, wheel/drag camera, minimap |

Tests (`node --test`, 22): hex math properties, camera maths (zoom keeps the cursor point fixed, pan clamping), RNG/noise determinism, heap order, movement and
A* optimality (checked against Dijkstra), downhill rivers, point symmetry, and 25 generated
maps checked for determinism, connectivity, spawn distance, village spacing and roads.
