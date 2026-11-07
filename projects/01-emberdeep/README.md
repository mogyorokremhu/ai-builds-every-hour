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

## Controls (current text mode)
Type keys then Enter (you can chain them, e.g. `ddddw`):
`w a s d` move · `q e z c` diagonals · `.` wait · `>` descend · `x` quit

## Architecture
| Module | Purpose |
|---|---|
| `geometry.py` | Rect, Bresenham lines, distances |
| `tiles.py` / `gamemap.py` | Tile types and the map with visibility memory |
| `dungeon.py` | Room-and-corridor generator |
| `fov.py` | Recursive shadowcasting field of view |
| `entities.py` | Player/monster entities and monster templates |
| `combat.py` | Melee resolution |
| `game.py` | Turn logic, levels, monster AI (renderer-independent) |
| `render_ascii.py` | Text renderer |
