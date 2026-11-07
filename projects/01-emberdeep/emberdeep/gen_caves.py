"""Cellular-automata cave generator.

1. Fill the map with random walls (``fill`` probability).
2. Run the classic 4-5 smoothing rule a few times: a cell becomes wall if it has 5+ wall
   neighbours (or very few walls nearby, to break up huge open areas early on).
3. Keep only the largest connected cave; everything else is filled in.
4. Retry with a new pattern if the cave is too small.
"""
from __future__ import annotations

import random
from collections import deque

from .gamemap import GameMap
from .tiles import FLOOR, WALL

Pos = tuple[int, int]


def wall_count(grid: list[list[bool]], x: int, y: int, r: int = 1) -> int:
    """Walls within Chebyshev radius ``r`` of (x, y), counting the cell itself and off-map."""
    h, w = len(grid), len(grid[0])
    n = 0
    for yy in range(y - r, y + r + 1):
        for xx in range(x - r, x + r + 1):
            if not (0 <= xx < w and 0 <= yy < h) or grid[yy][xx]:
                n += 1
    return n


def smooth(grid: list[list[bool]], early: bool) -> list[list[bool]]:
    h, w = len(grid), len(grid[0])
    out = [[True] * w for _ in range(h)]
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            near = wall_count(grid, x, y, 1)
            if early:
                far = wall_count(grid, x, y, 2)
                out[y][x] = near >= 5 or far <= 2
            else:
                out[y][x] = near >= 5
    return out


def regions(grid: list[list[bool]]) -> list[list[Pos]]:
    """Connected open regions (8-connectivity), largest first."""
    h, w = len(grid), len(grid[0])
    seen = [[False] * w for _ in range(h)]
    found: list[list[Pos]] = []
    for y in range(h):
        for x in range(w):
            if grid[y][x] or seen[y][x]:
                continue
            region: list[Pos] = []
            q = deque([(x, y)])
            seen[y][x] = True
            while q:
                cx, cy = q.popleft()
                region.append((cx, cy))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and not grid[ny][nx] and not seen[ny][nx]:
                            seen[ny][nx] = True
                            q.append((nx, ny))
            found.append(region)
    found.sort(key=len, reverse=True)
    return found


def generate(width: int, height: int, rng: random.Random, fill: float = 0.45,
             min_open: float = 0.32, tries: int = 12) -> tuple[GameMap, list[Pos]]:
    """Return a cave map and the list of its open cells (all mutually reachable)."""
    best: list[Pos] = []
    for _ in range(tries):
        grid = [[True if x in (0, width - 1) or y in (0, height - 1) else rng.random() < fill
                 for x in range(width)] for y in range(height)]
        for i in range(5):
            grid = smooth(grid, early=i < 3)
        regs = regions(grid)
        cave = regs[0] if regs else []
        if len(cave) > len(best):
            best = cave
        if len(best) >= width * height * min_open:
            break
    gmap = GameMap(width, height)
    for x, y in best:
        gmap.set(x, y, FLOOR)
    return gmap, sorted(best, key=lambda p: (p[1], p[0]))


def bfs_distances(gmap: GameMap, start: Pos) -> dict[Pos, int]:
    """Step distances over passable tiles (8-connectivity; closed doors count)."""
    dist = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                n = (x + dx, y + dy)
                if n not in dist and gmap.passable(*n):
                    dist[n] = dist[(x, y)] + 1
                    q.append(n)
    return dist


def sectors(cells: list[Pos], cell_w: int = 12, cell_h: int = 8) -> list[list[Pos]]:
    """Split open cells into coarse grid sectors so spawners can treat them like rooms."""
    buckets: dict[tuple[int, int], list[Pos]] = {}
    for x, y in cells:
        buckets.setdefault((x // cell_w, y // cell_h), []).append((x, y))
    return [buckets[k] for k in sorted(buckets) if len(buckets[k]) >= 6]
