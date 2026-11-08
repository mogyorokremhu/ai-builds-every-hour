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

## Phase 4 — Economy & objectives ✅
- [x] Village ownership drawn on the map (side-coloured flags) and counted in the roster header
- [x] Capture villages (move onto them, ends the move, undoable); income 2 + 2 per village per turn
- [x] Recruit units at your keep with gold (generated keep + castle hexes; blocked while an enemy holds the keep)
- [x] Healing in villages (+8); healer adjacency heal (+4, medic perk +8) at the start of your turn
- [x] Victory conditions: rout (no units and no way to recruit), hold ⅔ of villages for 4 turns, or turn limit with score (draws possible)
- [x] Day/night cycle affecting lawful/chaotic units (6 phases, ±25%, map tint, forecast-aware)
- [x] New chaotic unit: Rogue (skirmisher — ignores zones of control)
- [x] Economy panel (gold, income, villages, hold progress), recruit panel, day/night strip; save format v2 (v1 still loads)

## Phase 5 — AI opponent ✅
- [x] Utility AI: score every move+attack option (damage dealt, risk, terrain, village value)
- [x] Target focus (finish wounded units), retreat to heal when weak
- [x] Village grabbing and recruitment strategy (counter-picks, time-of-day aware, saves gold)
- [x] Difficulty levels; AI vs AI self-play harness in node for balance testing (`tools/selfplay.mjs`)
- [x] Influence maps (threat/control) and terrain-aware distance fields shared across AI decisions
- [x] AI plays in the browser with animations; either side can be Human or AI (spectator mode)
- [x] AI endgame awareness: play for score near the turn limit, contest enemy holds harder
- [x] AI keeps a reserve of units guarding its villages against raiders

## Phase 6 — Abilities & variety ✅
- [x] Unit abilities: charge (cavalry), volley (archers), fireball (mage, area), heal, shield wall — plus rally (swordsman) and envenom (rogue); cooldowns
- [x] Status effects: slowed, poisoned, rallied, braced (icons on tokens, roster, unit panel)
- [x] Fog of war with height-aware hex line of sight, explored memory and ambushes
- [x] Weather (rain lowers ranged damage, fog shortens sight and reach, storms; seeded fronts, forecast strip)
- [x] More terrain: ruins, fords, burning fields that spread and burn out (bridges ✅, castles/keeps ✅)
- [x] AI uses abilities (previews scored in gold units) and plays under fog of war
- [x] Ability UI: buttons + number keys, purple target rings, fireball blast preview, result tooltip

## Phase 6½ — Follow-ups found while building Phase 6
- [ ] Fog-aware spectating: "Show all" toggle for hot-seat review (logic in `spectate.js` ✅, UI hookup queued)
- [x] AI scouting under fog (`scouting.js`: frontier hexes become AI goals while no enemy is seen)
- [x] Floating damage/heal numbers per victim (`effects.js`)
- [ ] Ability animations (arrow rain, fireball burst, heal sparkles, pulses) — `abilityfx.js` builders + drawer ✅ with tests; hookup into main.js queued
- [ ] Balance pass of ability numbers from self-play (document in BALANCE.md) — hard vs easy fell from ~80% to ~60%; holds decide 19 of 20 battles

## Phase 7 — Campaign & presentation
- [x] Skirmish setup screen (`skirmish.js` logic, `screens.js` form, Skirmish… dialog in main.js)
- [x] Short campaign of 5 scenarios with carried-over veterans (`campaign.js`; Campaign… menu, progress saved in localStorage)
- [x] WebAudio sound effects synthesised in code (no asset files) — `sound.js`, Sound checkbox
- [x] Animations: attack lunges, floating damage/heal numbers, death fades (`effects.js`)
- [x] Colour themes: default / high contrast / colour-blind safe (`palette.js`, `theme-hook.js` Theme select, saved in localStorage)
- [ ] Keyboard controls (E/U/N/Tab/Esc done) + remaining accessibility: focus trap in menu dialog
- [x] Mobile/touch support (`touch.js` recogniser + `touch-hook.js` replaying gestures as mouse/wheel events)

## Phase 8 — Polish
- [ ] Browser smoke test in CI-like script form (`tests/browser-smoke.mjs` exists; add screenshots to docs)
- [ ] Balance pass from AI self-play statistics (document in BALANCE.md)
- [ ] Hot-seat multiplayer + shareable replay files (deterministic re-simulation)
- [ ] Full docs with screenshots; test coverage of all game-logic modules
