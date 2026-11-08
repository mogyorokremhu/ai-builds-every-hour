"""Procedural dungeon generation using random room placement + L-shaped tunnels."""
from __future__ import annotations

import random

from .gamemap import GameMap
from .geometry import Rect
from .tiles import FLOOR, STAIRS_DOWN


def carve_room(gmap: GameMap, room: Rect) -> None:
    """Set every inner cell of ``room`` to floor."""
    for x, y in room.inner():
        gmap.set(x, y, FLOOR)


def carve_tunnel(gmap: GameMap, a: tuple[int, int], b: tuple[int, int], rng: random.Random) -> None:
    """Carve an L-shaped corridor between two points (random elbow direction)."""
    (x1, y1), (x2, y2) = a, b
    if rng.random() < 0.5:
        corner = (x2, y1)
    else:
        corner = (x1, y2)
    for (sx, sy), (ex, ey) in ((a, corner), (corner, b)):
        for x in range(min(sx, ex), max(sx, ex) + 1):
            for y in range(min(sy, ey), max(sy, ey) + 1):
                gmap.set(x, y, FLOOR)


def generate(
    width: int,
    height: int,
    rng: random.Random,
    max_rooms: int = 18,
    min_size: int = 5,
    max_size: int = 11,
) -> tuple[GameMap, list[Rect]]:
    """Generate a map. Returns the map and the list of rooms (first room = player start)."""
    gmap = GameMap(width, height)
    rooms: list[Rect] = []
    for _ in range(max_rooms * 4):
        if len(rooms) >= max_rooms:
            break
        w = rng.randint(min_size, max_size)
        h = rng.randint(min_size, max_size - 2)
        x = rng.randint(0, width - w - 1)
        y = rng.randint(0, height - h - 1)
        room = Rect(x, y, w, h)
        if any(room.intersects(r, margin=1) for r in rooms):
            continue
        carve_room(gmap, room)
        if rooms:
            carve_tunnel(gmap, rooms[-1].center, room.center, rng)
        rooms.append(room)
    if rooms:
        sx, sy = rooms[-1].center
        gmap.set(sx, sy, STAIRS_DOWN)
        gmap.stairs = (sx, sy)
    return gmap, rooms
