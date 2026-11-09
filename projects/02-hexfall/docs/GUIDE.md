# Hexfall guide

Hexfall is a hex-grid tactics game in vanilla ES modules — no build step.

## Run it

```bash
cd projects/02-hexfall
python3 -m http.server 8000     # or: npm run serve
# open http://localhost:8000/
```

`npm test` runs the 209 unit tests (`node --test`). The URL hash is the map seed, e.g. `#7`.

## Playing

- Click a unit to select it, click a highlighted hex to move, click an enemy in range to attack.
- **E** end turn, **U** undo a move, **N** next unit, **Tab** cycle units, **Esc** cancel / close dialog.
- Recruit at your keep with the side-panel buttons; capture villages for income.
- Abilities appear under the day/night strip when a unit is selected.
- Toolbar: seed, New battle, Random map, Skirmish… (setup form), Campaign… (5 scenarios with veterans), Fog of war, Sound, Weather, per-side AI (Human / easy / normal / hard), Save / Load / Export / Import, Reset zoom.
- Win by routing the enemy, holding 4 villages for 4 turns, or leading on points after turn 30.
- Touch: tap = click, drag = pan, pinch = zoom, long-press = tooltip.
- Fog of war with two humans shows a pass-the-device curtain between turns.

## Tools

| Command | What it does |
|---|---|
| `node tools/selfplay.mjs --games 20` | AI vs AI statistics |
| `node tools/balance.mjs` | per-unit efficiency and side bias (see BALANCE.md) |
| `node tools/replay.mjs record\|check` | deterministic replay files; open them in `replay.html` |
| `node tools/coverage.mjs` | which logic modules lack tests |
| `node tools/screenshots.mjs` | captures `docs/img/{board,fog,contrast,mobile}.png` (needs Playwright and a static server on :8765) |
| `node tests/browser-smoke.mjs` | scripted real-click playthrough, fails on any page error |

Screenshots are generated locally rather than committed (the repo workflow only pushes text files).

## Architecture

Pure logic modules (`hex`, `map`, `game`, `combat`, `ai`, `fog`, `status`, …) have no DOM access and are unit tested.
`main.js` owns the DOM; features that were added later hook in through small `*-hook.js` modules
(theme, touch, focus, spectate, hotseat, ability FX) that wrap prototypes or listen to events, so `main.js` stays untouched.
