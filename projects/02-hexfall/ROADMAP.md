# Hexfall Roadmap

Target: ~2–3 days of hourly work (40–70 runs). Each run should tick off several items.
Vanilla ES modules only; game logic stays DOM-free so it can be tested with `node --test`.

## Phase 1 — Map engine ✅
- [x] Axial/cube hex math (distance, neighbours, lines, rings, spirals, rotation, pixel/offset conversion)
- [x] Seeded RNG + string seeds; value noise with octaves
- [x] Terrain table (move cost, defence, sight blocking, height, colour)
- [x] `HexMap` with JSON round trip and ASCII dump
- [x] Pathfinding: binary heap, Dijkstra reachable area (free first step), A*, flood fill
- [x] Map generator: noise terrain, largest-region check, opposite deployment zones, villages, roads
- [x] Canvas renderer with terrain decorations, zone outlines, reach/path overlays
- [x] Browser map preview (seed box, random map, hover info, click-to-preview movement)
- [x] Rivers that flow downhill to the sea (pool into shallows in hollows; roads cross on bridges)
- [x] Map symmetry option for fair competitive maps (point-mirrored generation, `Symmetric` checkbox)
- [x] Camera: zoom and pan for big maps (wheel + drag, clamped), minimap with viewport box and click-to-jump

## Phase 2 — Units & turns ✅
- [x] Unit types: spearman, swordsman, archer, cavalry, mage, healer (HP, attack, defence, MP, range, cost, traits)
- [x] Two sides, deployment on spawn zones, unit roster panel (click to focus)
- [x] Turn system: select unit → move (several times while MP lasts) → act → end turn; undo moves step by step
- [x] Zone of control (entering a hex next to an enemy ends movement); pass through friends, enemies block
- [x] Units drawn as tokens with HP pips, side colours, veteran stars; selection, eased move animation
- [x] Game state object fully serialisable (save/load to localStorage, autosave + resume, export/import JSON)

## Phase 3 — Combat ✅
- [x] Attack resolution: damage = attack × modifiers × roll (±20%, seeded) − armour; terrain defence; spears ×1.5 vs mounts; magic ignores terrain
- [x] Ranged attacks with line of sight (forests/villages block unless you stand higher, mountains always); high ground +1 range
- [x] Counter-attacks (same kind, if the defender can reach); flanking +10% per extra adjacent ally (max 3)
- [x] Damage preview tooltip before attacking (exact forecast over all 25 outcomes: damage range, kill & death chance)
- [x] Experience and promotions (veteran: type perk; elite: +1/+1; +15% HP and full heal per level)
- [x] Combat log panel

## Phase 4 — Economy & objectives
- [ ] Village ownership drawn on the map (side-coloured flags) and counted in the roster header
- [ ] Capture villages (move onto them); income per village per turn
- [ ] Recruit units at your keep with gold
- [x] Healing in villages (+8); healer adjacency heal (+4, medic perk +8) at the start of your turn
- [ ] Victory conditions: rout the enemy (done), hold villages for N turns, or turn limit with score
- [ ] Day/night cycle affecting lawful/chaotic units

## Phase 5 — AI opponent
- [ ] Utility AI: score every move+attack option (damage dealt, risk, terrain, village value)
- [ ] Target focus (finish wounded units), retreat to heal when weak
- [ ] Village grabbing and recruitment strategy
- [ ] Difficulty levels; AI vs AI self-play harness in node for balance testing
- [ ] Influence maps (threat/safety) shared across AI decisions

## Phase 6 — Abilities & variety
- [ ] Unit abilities: charge (cavalry), volley (archers), fireball (mage, area), heal, shield wall
- [ ] Status effects: slowed, poisoned, rallied
- [ ] Fog of war with shadowcast-style hex line of sight
- [ ] Weather (rain lowers ranged accuracy, fog shortens sight)
- [ ] More terrain: bridges, castles, ruins

## Phase 7 — Campaign & presentation
- [ ] Skirmish setup screen (map size, seed, armies, AI level)
- [ ] Short campaign of 5 scenarios with carried-over veterans
- [ ] WebAudio sound effects synthesised in code (no asset files)
- [ ] Animations: attack lunges (done), damage numbers, death fades
- [ ] Keyboard controls (E/U/N/Tab/Esc done) + accessibility pass (focus, high-contrast palette)
- [ ] Mobile/touch support

## Phase 8 — Polish
- [ ] Browser smoke test in CI-like script form (`tests/browser-smoke.mjs` exists; add screenshots to docs)
- [ ] Balance pass from AI self-play statistics (document in BALANCE.md)
- [ ] Hot-seat multiplayer + shareable replay files (deterministic re-simulation)
- [ ] Full docs with screenshots; test coverage of all game-logic modules
