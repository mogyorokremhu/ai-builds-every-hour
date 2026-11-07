"""Tile definitions for the dungeon map."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Tile:
    name: str
    glyph: str
    walkable: bool
    transparent: bool


WALL = Tile("wall", "#", walkable=False, transparent=False)
FLOOR = Tile("floor", ".", walkable=True, transparent=True)
DOOR = Tile("door", "+", walkable=False, transparent=False)        # closed: bump to open
OPEN_DOOR = Tile("open door", "'", walkable=True, transparent=True)
STAIRS_DOWN = Tile("stairs down", ">", walkable=True, transparent=True)
FUNGUS = Tile("fungus", '"', walkable=True, transparent=True)
LAVA = Tile("lava", "~", walkable=False, transparent=True)
ALTAR = Tile("altar", "_", walkable=True, transparent=True)
RUBBLE = Tile("rubble", ",", walkable=True, transparent=True)

#: Tiles counted as open ground by the generators and spawners.
FLOOR_LIKE = frozenset({"floor", "fungus", "rubble"})

#: Door tiles (closed doors block movement and sight until opened).
DOOR_NAMES = frozenset({"door", "open door"})

#: Every tile, keyed by glyph (glyphs are unique) — used by save files.
TILES_BY_GLYPH: dict[str, Tile] = {t.glyph: t for t in (
    WALL, FLOOR, DOOR, OPEN_DOOR, STAIRS_DOWN, FUNGUS, LAVA, ALTAR, RUBBLE)}
