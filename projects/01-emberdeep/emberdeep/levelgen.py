"""Level assembly: pick a generator for the theme, decorate, place stairs.

Every generator produces a :class:`Layout` with the same shape, so the game's spawners
don't care whether a level is made of rooms or caves:

* ``areas`` — groups of open cells (rooms, or cave sectors); ``areas[0]`` holds the start.
* ``rooms`` — the rectangular rooms (empty for caves), used for vaults/special rooms.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

from . import dungeon, gen_bsp, gen_caves
from .gamemap import GameMap
from .geometry import Rect
from .themes import Theme
from .tiles import FLOOR, FLOOR_LIKE, FUNGUS, LAVA, RUBBLE, STAIRS_DOWN

Pos = tuple[int, int]


@dataclass
class Layout:
    gmap: GameMap
    start: Pos
    areas: list[list[Pos]]
    rooms: list[Rect] = field(default_factory=list)
    generator: str = "rooms"


def open_cells(gmap: GameMap) -> list[Pos]:
    return [(x, y) for y in range(gmap.height) for x in range(gmap.width)
            if gmap.tiles[y][x].name in FLOOR_LIKE]


def reachable(gmap: GameMap, start: Pos) -> set[Pos]:
    return set(gen_caves.bfs_distances(gmap, start))


def _rooms_layout(gmap: GameMap, rooms: list[Rect], kind: str) -> Layout:
    areas = [list(r.inner()) for r in rooms]
    return Layout(gmap, rooms[0].center, areas, list(rooms), kind)


def _caves_layout(width: int, height: int, rng: random.Random) -> Layout:
    gmap, cells = gen_caves.generate(width, height, rng)
    start = rng.choice(cells)
    dist = gen_caves.bfs_distances(gmap, start)
    stairs = max(dist, key=lambda p: (dist[p], p))
    gmap.set(*stairs, STAIRS_DOWN)
    gmap.stairs = stairs
    sectors = gen_caves.sectors([c for c in cells if c != stairs])
    sectors.sort(key=lambda s: start not in s)  # start sector first
    if not sectors or start not in sectors[0]:
        sectors.insert(0, [start])
    return Layout(gmap, start, sectors, [], "caves")


def decorate(layout: Layout, theme: Theme, rng: random.Random) -> int:
    """Scatter the theme's decoration. Lava never cuts the level apart. Returns tiles changed."""
    kind, amount = theme.decoration, theme.decoration_amount
    if not kind or amount <= 0:
        return 0
    gmap = layout.gmap
    protected = {layout.start, gmap.stairs}
    cells = [c for c in open_cells(gmap) if c not in protected]
    target = int(len(cells) * amount)
    changed = 0
    if kind in ("fungus", "rubble"):
        tile = FUNGUS if kind == "fungus" else RUBBLE
        # grow in small clumps
        while changed < target and cells:
            x, y = rng.choice(cells)
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                if changed >= target:
                    break
                if gmap.get(x + dx, y + dy).name == "floor" and (x + dx, y + dy) not in protected:
                    gmap.set(x + dx, y + dy, tile)
                    changed += 1
        return changed
    # lava pools: add blob by blob and undo any blob that disconnects the level
    before = len(reachable(gmap, layout.start))
    attempts = 0
    while changed < target and attempts < 60:
        attempts += 1
        cx, cy = rng.choice(cells)
        blob = [(cx + dx, cy + dy) for dx in range(-2, 3) for dy in range(-1, 2)
                if abs(dx) + abs(dy) <= 2 and rng.random() < 0.8]
        blob = [p for p in blob if gmap.get(*p).name in FLOOR_LIKE and p not in protected
                and all(abs(p[0] - q[0]) > 1 or abs(p[1] - q[1]) > 1 for q in protected)]
        if not blob:
            continue
        old = {p: gmap.get(*p) for p in blob}
        for p in blob:
            gmap.set(*p, LAVA)
        now = reachable(gmap, layout.start)
        if gmap.stairs not in now or len(now) < before - len(blob):
            for p, t in old.items():
                gmap.set(*p, t)
            continue
        before = len(now)
        changed += len(blob)
    if changed:
        for area in layout.areas:
            area[:] = [p for p in area if gmap.walkable(*p)]
    return changed


def generate_level(width: int, height: int, rng: random.Random, theme: Theme) -> Layout:
    keys, weights = zip(*theme.generators)
    kind = rng.choices(keys, weights=weights)[0]
    if kind == "caves":
        layout = _caves_layout(width, height, rng)
    elif kind == "bsp":
        gmap, rooms = gen_bsp.generate(width, height, rng)
        layout = _rooms_layout(gmap, rooms, "bsp")
    else:
        gmap, rooms = dungeon.generate(width, height, rng)
        layout = _rooms_layout(gmap, rooms, "rooms")
    decorate(layout, theme, rng)
    if layout.gmap.get(*layout.start).name != "floor":
        layout.gmap.set(*layout.start, FLOOR)
    return layout
