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
DOOR = Tile("door", "+", walkable=True, transparent=False)
STAIRS_DOWN = Tile("stairs down", ">", walkable=True, transparent=True)
