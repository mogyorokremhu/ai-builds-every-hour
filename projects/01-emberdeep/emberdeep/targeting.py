"""Targeting helpers: projectile paths, blast areas and a cursor for the UI."""
from __future__ import annotations

from dataclasses import dataclass

from .gamemap import GameMap
from .geometry import bresenham, chebyshev


def projectile_path(gmap: GameMap, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    """Cells a projectile crosses from ``start`` (exclusive) towards ``end``, stopping at walls."""
    path: list[tuple[int, int]] = []
    for p in bresenham(*start, *end)[1:]:
        if not gmap.walkable(*p):
            break
        path.append(p)
    return path


def blast_area(gmap: GameMap, center: tuple[int, int], radius: int) -> list[tuple[int, int]]:
    """Walkable cells within ``radius`` (round-ish) of ``center`` with line of effect to it."""
    cx, cy = center
    cells: list[tuple[int, int]] = []
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 > radius * radius + radius:
                continue
            if not gmap.walkable(x, y):
                continue
            if (x, y) == center or projectile_path(gmap, center, (x, y))[-1:] == [(x, y)]:
                cells.append((x, y))
    return cells


@dataclass
class Cursor:
    """A movable targeting cursor bounded to the map and a max range from an origin."""

    origin: tuple[int, int]
    x: int
    y: int
    max_range: int
    width: int
    height: int

    @property
    def pos(self) -> tuple[int, int]:
        return (self.x, self.y)

    def move(self, dx: int, dy: int) -> None:
        nx = min(max(self.x + dx, 0), self.width - 1)
        ny = min(max(self.y + dy, 0), self.height - 1)
        if chebyshev(self.origin, (nx, ny)) <= self.max_range:
            self.x, self.y = nx, ny

    def jump(self, pos: tuple[int, int]) -> None:
        self.x, self.y = pos

    def cycle(self, candidates: list[tuple[int, int]]) -> None:
        """Jump to the next candidate (e.g. visible monsters) after the current position."""
        if not candidates:
            return
        if self.pos in candidates:
            idx = (candidates.index(self.pos) + 1) % len(candidates)
        else:
            idx = 0
        self.jump(candidates[idx])
