"""Small geometry helpers: points, rectangles and lines."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Rect:
    """Axis-aligned rectangle using inclusive-exclusive bounds."""

    x: int
    y: int
    w: int
    h: int

    @property
    def x2(self) -> int:
        return self.x + self.w

    @property
    def y2(self) -> int:
        return self.y + self.h

    @property
    def center(self) -> tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h // 2)

    def inner(self) -> Iterator[tuple[int, int]]:
        """Yield every tile inside the rectangle, excluding its 1-tile border."""
        for yy in range(self.y + 1, self.y2 - 1):
            for xx in range(self.x + 1, self.x2 - 1):
                yield xx, yy

    def intersects(self, other: "Rect", margin: int = 0) -> bool:
        return (
            self.x - margin < other.x2
            and self.x2 + margin > other.x
            and self.y - margin < other.y2
            and self.y2 + margin > other.y
        )

    def contains(self, x: int, y: int) -> bool:
        return self.x <= x < self.x2 and self.y <= y < self.y2


def bresenham(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    """Return the tiles on a straight line from (x0, y0) to (x1, y1), inclusive."""
    points: list[tuple[int, int]] = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return points
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def chebyshev(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Distance where diagonal moves cost 1 (king moves)."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
