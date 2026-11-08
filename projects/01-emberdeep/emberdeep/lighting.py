"""Wall braziers: fixed light sources that light up the area around them.

A brazier (``*``) replaces a wall tile at the edge of a room or cave. Everything a brazier
can see within :data:`BRAZIER_RADIUS` is *lit*: you can see lit cells from far away (up to
:data:`emberdeep.fov.LIT_SIGHT`) even when your own torch is guttering, as long as you have
line of sight. Lit cells are derived from the map itself, so save files need nothing extra.
"""
from __future__ import annotations

import random

from .gamemap import GameMap
from .tiles import BRAZIER, FLOOR_LIKE

BRAZIER_RADIUS = 5
ORTHO = ((1, 0), (-1, 0), (0, 1), (0, -1))

#: Theme key -> (min, max) braziers per level.
BRAZIERS_BY_THEME: dict[str, tuple[int, int]] = {
    "cellars": (0, 2),
    "fungal": (0, 1),
    "magma": (2, 4),
    "heart": (2, 5),
}


def _floorish(gmap: GameMap, x: int, y: int) -> bool:
    return gmap.get(x, y).name in FLOOR_LIKE


def brazier_spots(gmap: GameMap, protected: set[tuple[int, int]] | None = None) -> list[tuple[int, int]]:
    """Wall cells that can hold a brazier without opening a view through the wall.

    The wall must touch open floor on exactly one orthogonal side, with solid wall behind it.
    """
    protected = protected or set()
    spots: list[tuple[int, int]] = []
    for y in range(1, gmap.height - 1):
        for x in range(1, gmap.width - 1):
            if gmap.tiles[y][x].name != "wall" or (x, y) in protected:
                continue
            fronts = [(dx, dy) for dx, dy in ORTHO if _floorish(gmap, x + dx, y + dy)]
            if len(fronts) != 1:
                continue
            dx, dy = fronts[0]
            if gmap.get(x - dx, y - dy).name != "wall":
                continue
            # the two side neighbours must be wall too (keeps braziers off corridor mouths)
            if gmap.get(x + dy, y + dx).name != "wall" or gmap.get(x - dy, y - dx).name != "wall":
                continue
            spots.append((x, y))
    return spots


def place_braziers(gmap: GameMap, rng: random.Random, count: int,
                   protected: set[tuple[int, int]] | None = None) -> list[tuple[int, int]]:
    """Turn up to ``count`` suitable walls into braziers, spread apart. Returns their cells."""
    spots = brazier_spots(gmap, protected)
    rng.shuffle(spots)
    placed: list[tuple[int, int]] = []
    for p in spots:
        if len(placed) >= count:
            break
        if all(max(abs(p[0] - q[0]), abs(p[1] - q[1])) > 2 * BRAZIER_RADIUS for q in placed):
            gmap.set(*p, BRAZIER)
            placed.append(p)
    return placed


def braziers(gmap: GameMap) -> list[tuple[int, int]]:
    """Positions of every brazier on the map."""
    return [(x, y) for y in range(gmap.height) for x in range(gmap.width)
            if gmap.tiles[y][x].name == "brazier"]


def compute_lit(gmap: GameMap) -> frozenset[tuple[int, int]]:
    """Every cell lit by some brazier on the map (line of sight within the brazier radius)."""
    from .fov import compute_fov

    saved = [row[:] for row in gmap.explored]
    lit: set[tuple[int, int]] = set()
    for bx, by in braziers(gmap):
        compute_fov(gmap, bx, by, BRAZIER_RADIUS)
        for y in range(max(0, by - BRAZIER_RADIUS), min(gmap.height, by + BRAZIER_RADIUS + 1)):
            row = gmap.visible[y]
            for x in range(max(0, bx - BRAZIER_RADIUS), min(gmap.width, bx + BRAZIER_RADIUS + 1)):
                if row[x]:
                    lit.add((x, y))
    gmap.explored = saved
    gmap.clear_visibility()
    return frozenset(lit)


def braziers_for_theme(theme_key: str, rng: random.Random) -> int:
    """A random number of braziers for a theme, from its (low, high) range."""
    lo, hi = BRAZIERS_BY_THEME.get(theme_key, (0, 2))
    return rng.randint(lo, hi)
