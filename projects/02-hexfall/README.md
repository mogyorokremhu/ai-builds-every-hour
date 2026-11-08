# ⬡ Hexfall

A turn-based **hex-grid tactics game** for the browser, in plain JavaScript ES modules —
no build step, no dependencies. Two armies deploy on a procedurally generated battlefield
of plains, forests, hills, rivers and villages; capture villages for income, use terrain
for cover, and outmanoeuvre an AI opponent.

**Status:** 🚧 Phases 1–6 ✅ — a complete battle against a **utility AI** (or hot-seat): seven unit
types deploy from castles, move under zones of control, fight with terrain, flanking, line of sight,
counter-attacks and a **day/night cycle**; every unit has a special **ability** (charge, volley,
fireball, heal, shield wall, rally, envenom) and can suffer **status effects** (poisoned, slowed,
rallied, braced); seeded **weather** fronts (rain, fog, storms) and optional **fog of war** with
ambushes; fireballs set **fields burning**. Capture villages for **gold**, **recruit** at your keep, and
win by routing the enemy, **holding villages** or **leading on points** at the turn limit. A node
**self-play harness** pits AIs against each other for balance testing. Next: Phase 7 (skirmish setup,
campaign, sound, effects). Built hourly, see [ROADMAP.md](ROADMAP.md).

## Run
```bash
cd projects/02-hexfall
python3 -m http.server 8000     # any static server works (ES modules need http://, not file://)
# open http://localhost:8000/#7  (the part after # is the map seed; text seeds work too)
npm test                        # or: node --test tests/*.test.js   (Node 18+)
node tools/selfplay.mjs --games 20 --red hard --blue easy   # AI vs AI statistics
```

**How to play:** you are Red, the AI plays Blue (switch either side between *Human* and AI
easy/normal/hard with the selectors; two AIs make a spectator match, two humans a hot-seat game). Red moves first. Click one of your units: yellow hexes show where it
can go, red rings mark enemies it can attack this turn. Click a yellow hex to move (you can keep
moving while move points last), or click a ringed enemy to attack — melee units step next to the
target by themselves, choosing the best hex. Hover an enemy to see the exact damage forecast.
Select a unit and press **1** (or its button under the economy panel) to use its **ability**: purple
rings mark valid targets and hovering one previews the result. Press **E** to end the turn, **U** to undo a move, **N**/**Tab** for the next ready unit, **Esc**
to deselect. The mouse wheel zooms, dragging pans, the minimap jumps. The battle autosaves; Save/Load
use a browser slot, Export/Import a JSON file.

**Economy & objectives:** move onto a village to capture it (it flies your flag; capturing ends the
move). At the start of each of your turns you collect 2 gold + 2 per village. Spend it in the
*Recruit* panel: the recruit appears on a free castle hex around your keep (hover a button to see
them) and can act next turn — but nobody can recruit while an enemy stands on their keep. You win by
**routing** the enemy (no units and no way to recruit), **holding ⅔ of the villages** for 4 of your
turns in a row, or by having the higher **score** (army value + 12 per village + gold) after turn 30.

**Day and night:** turns cycle dawn → morning → afternoon → dusk → first watch → second watch. Lawful
units deal +25% damage in daylight and −25% at night; chaotic units the reverse; neutral units do not
care. The strip above the economy panel shows the next six turns.

## Units
| Unit | HP | Melee | Ranged (range) | Armour | MP | Cost | Alignment | Special | Ability | Veteran perk |
|---|---|---|---|---|---|---|---|---|---|---|
| Spearman | 34 | 9 | — | 2 | 5 | 14 | lawful | ×1.5 damage to mounted units | Shield wall | Phalanx: +2 armour |
| Swordsman | 40 | 11 | — | 3 | 5 | 17 | lawful | | Rally | Blademaster: +3 melee |
| Archer | 28 | 4 | 8 (3) | 1 | 5 | 15 | neutral | needs line of sight; sight 5 | Volley | Longshot: +1 range |
| Cavalry | 38 | 10 | — | 2 | 8 | 20 | lawful | mounted: forest/swamp +1 MP; sight 5 | Charge | Outrider: +1 MP |
| Mage | 24 | 3 | 11 (2) | 0 | 5 | 20 | chaotic | magic ignores terrain defence | Fireball | Arcanist: +3 ranged |
| Healer | 26 | 4 | — | 1 | 5 | 16 | lawful | heals adjacent allies 4/turn | Heal | Medic: heals 8 |
| Rogue | 30 | 8 | — | 1 | 6 | 15 | chaotic | skirmisher: ignores zones of control; sight 5 | Envenom | Backstab: +2 melee, +1 MP |

## Abilities
Using an ability takes the unit's action for the turn (like attacking). Most then recharge for a few of
its own turns.

| Ability | Unit | Cooldown | Effect |
|---|---|---|---|
| 🐎 Charge | Cavalry | 2 | Melee attack after moving this turn; **both** sides deal ×1.5 damage |
| 🏹 Volley | Archer | 3 | 75% shot at the target **and every enemy next to it**; slows the target; no counter |
| 🔥 Fireball | Mage | 3 | Hex in range and sight: full damage there, 60% on the six around it — **allies too**; dry plains and forests catch fire; no counter |
| ✚ Heal | Healer | — | +12 HP (medics more) to an adjacent ally, cures poison |
| 🛡 Shield wall | Spearman | 3 | The spearman and adjacent allies are **braced** until its next turn |
| ⚑ Rally | Swordsman | 3 | The swordsman and adjacent allies are **rallied** this turn and the next |
| ☠ Envenom | Rogue | 2 | Melee strike that **poisons** a surviving target for 3 turns |

**Status effects** (icons above the token, details in the unit panel):
**poisoned** — −6 HP at the start of each own turn, never below 1; a village or healer cures it instead of
healing. **Slowed** — half move points and −25% damage for its next turn. **Rallied** — +20% damage.
**Braced** — 35% less damage taken.

## Weather, fire and fog of war
- **Weather** comes in seeded 3-turn fronts (the first is always clear): *rain* (ranged −20%, sight −1),
  *fog* (ranged reach −1, sight −2) and *storms* (ranged −30%, reach −1, sight −2). It is derived from the
  battle seed and the turn number, so replays and saves need no extra state. The strip at the top of the
  panel shows the next six turns. Untick *Weather* for always-clear battles.
- **Fire:** a fireball in dry weather sets plains and forests alight for 3 turns. Burning hexes cost +2 MP
  to enter and burn units that start their turn there for 6 (never below 1 HP). Each round a fire may
  spread to flammable neighbours (20%); a forest that burns out becomes plains; rain and storms put
  every fire out.
- **Fog of war** (*Fog of war* checkbox, off by default): each side sees what its units see (sight 4–5,
  +1 on hills, minus the weather, blocked by forests/villages/mountains as for arrows) plus the hexes
  around its own villages. Unseen ground is dimmed, never-seen ground black; hidden enemies cannot be
  attacked and are left out of the movement preview — walking into one's zone of control is an
  **ambush**: the move stops there and cannot be undone. The AI plays by the same rules (it only reacts
  to enemies it can see). In hot-seat games the board shows the side to move.

## Combat rules
- **Damage** of one strike = attack × flanking × (1 − target terrain defence) × anti-cavalry × time of day
  × statuses × weather (ranged) × ability × roll − armour,
  rounded, at least 1. The roll is one of 0.8 / 0.9 / 1.0 / 1.1 / 1.2, drawn from the game's seeded RNG.
- **Counter-attack:** if the defender survives and has the same kind of attack that reaches the
  attacker (melee next to it, or ranged within its range and line of sight), it strikes back once.
- **Flanking:** +10% melee damage for every *other* friendly unit next to the target (max +30%).
- **Line of sight:** forests and villages block shots unless the shooter stands higher (hills);
  mountains always block. Lines along hex edges count as clear if either side is clear.
  **High ground** (hills) gives ranged units +1 range.
- **Zone of control:** a unit that steps next to an enemy stops there (skirmishers excepted). Friends can be passed through.
- **Experience:** 1 XP × enemy level for every exchange survived, 8 × enemy level for a kill.
  20 XP → **Veteran** (type perk), 45 more → **Elite** (+1 attack, +1 armour); each promotion adds
  15% HP and heals fully.
- **Healing** at the start of your turn: +8 in a village, +4 next to a healer (the best one applies).
- The **forecast** tooltip enumerates all 25 roll combinations exactly (a dead target never
  counters), giving damage ranges, kill chance and your risk of dying.

## The AI
`src/ai.js` is a **utility AI**: for every unit it scores each reachable hex (stay, move) and each
attack from each hex, then plays the single best option across the whole army, one action at a time
(so archers soften targets before the swordsmen move in). Considerations:
- **Trade value** of an attack in gold: expected damage × (target cost / HP) + kill chance × target
  cost, minus the same for the expected counter-damage and death chance (weighted by risk appetite);
  a bonus for finishing badly wounded units;
- **Threat** at the destination from `src/influence.js`'s threat map (what every enemy could reach and
  hit next turn, at next turn's time of day), discounted by terrain defence and armour;
- **Terrain defence**, **villages** to capture (enemy-held ones count extra), **healing** (wounded units
  value villages and healers; healers value standing next to wounded friends), **keep defence** when
  enemies approach it;
- **Abilities**: every ability target from every reachable hex is previewed (`abilityPreview`) and
  scored in the same gold units — friendly fire counts 1.5× against, heals by HP restored, shield walls
  by the threat they absorb, rallies by the allies that can still strike; abilities with a cooldown
  must beat a plain attack by a margin;
- **Endgame**: within 3 turns of the limit a side that leads on points becomes more careful and one
  that trails chases villages harder; while the enemy is building a village hold its villages are
  worth extra; owned villages with raiders within 5 hexes are worth **guarding**;
- **Progress** along terrain-aware distance fields: healthy units advance on enemies, villages and the
  enemy keep; units below 35% HP fall back towards safe villages and healers.

Recruiting counter-picks (spearmen against cavalry, cavalry against archers), favours units whose
time of day is coming, avoids piling up one type, and **saves gold** for the unit it wants most unless
its army is thin. Difficulty sets random noise, risk appetite and focus fire (Easy / Normal / Hard).

`node tools/selfplay.mjs` runs AI-vs-AI battles headless (`src/selfplay.js`): win rates, end reasons,
battle length, recruits, kills per unit type and abilities used. 20 symmetric games, normal vs normal: **55% / 45%**,
avg 15 turns, 19 of them decided by village holds; shield walls and heals are the most used abilities.
Hard beat easy about 80% of the time before abilities and 6 of 10 since — the ability balance pass is next on
the roadmap.

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
6. **Castles:** each deployment zone becomes a castle — its first hex the **keep** (45% defence,
   high ground), the others castle hexes (35%) where recruits appear.
7. **Ruins and fords:** two ruined forts in no-man's-land (25% defence, block sight, no income) and two
   **fords** where a river can be waded for 2 MP between dry banks (never next to a bridge).
8. **Symmetric mode** (`symmetric: true`, the *Symmetric* checkbox) point-mirrors the map
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
| Castle | 1 | 35% | recruits appear here |
| Keep | 1 | 45% | high ground, blocks sight; hold the enemy's to stop its recruiting |
| Ruins | 1 | 25% | blocks sight |
| Ford | 2 | −5% | shallow river crossing |
| Swamp / Shallows / River | 3 | −10% | fighting knee-deep is a bad idea |
| Water / Mountain | — | — | impassable (mountains block sight) |
| *burning* (plains/forest) | +2 | — | 6 damage at turn start, spreads, burns out (forest → plains) |

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
| `src/game.js` | `Game`: deployment, turns, move/undo, captures, recruiting, attack plans, upkeep (income, healing, holds), victory, JSON |
| `src/economy.js` | Rules table, village ownership, income, keep and recruit hexes, hold target, battle score |
| `src/timeofday.js` | Six-phase day/night cycle and lawful/chaotic damage multipliers |
| `src/influence.js` | Strike/threat/control maps and terrain-aware distance fields for the AI |
| `src/ai.js` | Utility AI player (`AIPlayer`): option scoring, recruiting, difficulty presets |
| `src/selfplay.js` | Headless AI-vs-AI matches and series reports (`tools/selfplay.mjs` CLI) |
| `src/save.js` | Save text, storage slots (localStorage or the in-memory `MemoryStorage`) |
| `src/animate.js` | Pure tweening: eased moves along routes, attack lunges |
| `src/abilities.js` | Seven abilities: targets, cooldowns, exact/expected previews, seeded resolution, fire |
| `src/status.js` | Status effects (poisoned, slowed, rallied, braced): durations, ticks, multipliers |
| `src/weather.js` | Seeded weather fronts, their combat/sight effects and the forecast |
| `src/fog.js` | Fog of war: sight radius, per-side visible sets, explored memory |
| `src/main.js` | Browser UI: battle controls, roster, log, forecast tooltip, animations, keys, saves, camera, minimap |

Tests (`node --test`, 128): all seven abilities (targets, previews vs. real rolls, friendly fire, fire
spread and burn-out, cooldowns over turns, save round trips), status ticks and multipliers, weather
determinism/weights/effects, fog of war (sight, hidden targets, ambushes, explored memory, AI under fog),
ruins and fords, AI ability choices and endgame/guard scoring; economy (captures + undo, income, recruiting rules, keep blocking, hold
and turn-limit victories, draws, v1 save compatibility), day/night damage, influence maps, AI
behaviour (focus fire, retreat to heal, village grabbing, deterministic self-play), skirmishers; hex math properties, camera maths, RNG/noise determinism, heap
order, A* optimality, downhill rivers, point symmetry, 25 generated maps checked for
determinism and playability; unit stats and promotions; movement with ZOC, blocking and mounted
costs; damage rules, flanking, line of sight (incl. symmetry over thousands of pairs), exact
forecasts vs. hand-computed odds, seeded attack resolution; turns, undo, healing, victory, save
round trips where a loaded game replays identically; animation tweening.

`tests/browser-smoke.mjs` drives the real page in Chromium (Playwright): it selects, moves, undoes,
then plays a battle with mouse clicks and keys, recruits from the panel, hands Blue to the AI and
waits for it to play its turn, saves and loads, then starts a fogged battle (checks enemies are
hidden) and raises a shield wall with the **1** key — and fails on any page error.
