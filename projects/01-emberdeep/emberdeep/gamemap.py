"""The GameMap holds tiles plus visibility/exploration state."""
from __future__ import annotations

from .tiles import WALL, Tile


class GameMap:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles: list[list[Tile]] = [[WALL] * width for _ in range(height)]
        self.visible: list[list[bool]] = [[False] * width for _ in range(height)]
        self.explored: list[list[bool]] = [[False] * width for _ in range(height)]
        self.stairs: tuple[int, int] | None = None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, x: int, y: int) -> Tile:
        return self.tiles[y][x] if self.in_bounds(x, y) else WALL

    def set(self, x: int, y: int, tile: Tile) -> None:
        if self.in_bounds(x, y):
            self.tiles[y][x] = tile

    def walkable(self, x: int, y: int) -> bool:
        return self.get(x, y).walkable

    def passable(self, x: int, y: int) -> bool:
        """Walkable, or a closed door a creature could open (used for pathing/connectivity)."""
        t = self.get(x, y)
        return t.walkable or t.name == "door"

    def is_closed_door(self, x: int, y: int) -> bool:
        return self.get(x, y).name == "door"

    def transparent(self, x: int, y: int) -> bool:
        return self.get(x, y).transparent

    def clear_visibility(self) -> None:
        for row in self.visible:
            for i in range(len(row)):
                row[i] = False

    def mark_visible(self, x: int, y: int) -> None:
        if self.in_bounds(x, y):
            self.visible[y][x] = True
            self.explored[y][x] = True
