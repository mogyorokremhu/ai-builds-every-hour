"""Tile definitions for the dungeon map."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Tile:
    name: str
    glyph: str
    walkable: bool
    transparent: bool
    code: str = ""          # save-file character when the glyph is shared (default: the glyph)

    @property
    def save_code(self) -> str:
        return self.code or self.glyph


WALL = Tile("wall", "#", walkable=False, transparent=False)
FLOOR = Tile("floor", ".", walkable=True, transparent=True)
DOOR = Tile("door", "+", walkable=False, transparent=False)        # closed: bump to open
OPEN_DOOR = Tile("open door", "'", walkable=True, transparent=True)
STAIRS_DOWN = Tile("stairs down", ">", walkable=True, transparent=True)
FUNGUS = Tile("fungus", '"', walkable=True, transparent=True)
LAVA = Tile("lava", "~", walkable=False, transparent=True)
ALTAR = Tile("altar", "_", walkable=True, transparent=True)
RUBBLE = Tile("rubble", ",", walkable=True, transparent=True)
LOCKED_DOOR = Tile("locked door", "+", walkable=False, transparent=False, code="L")  # key or force
BRAZIER = Tile("brazier", "*", walkable=False, transparent=True)  # lights the room around it

#: Tiles counted as open ground by the generators and spawners.
FLOOR_LIKE = frozenset({"floor", "fungus", "rubble"})

#: Door tiles (closed doors block movement and sight until opened).
DOOR_NAMES = frozenset({"door", "open door"})

ALL_TILES = (WALL, FLOOR, DOOR, OPEN_DOOR, STAIRS_DOWN, FUNGUS, LAVA, ALTAR, RUBBLE, LOCKED_DOOR, BRAZIER)

#: Every tile, keyed by its save code (unique) — used by save files.
TILES_BY_CODE: dict[str, Tile] = {t.save_code: t for t in ALL_TILES}
#: Kept for older callers: same mapping (codes equal glyphs for all original tiles).
TILES_BY_GLYPH = TILES_BY_CODE

assert len(TILES_BY_CODE) == len(ALL_TILES), "tile save codes must be unique"
