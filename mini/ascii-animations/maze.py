#!/usr/bin/env python3
"""A maze carves itself (randomised depth-first search), then a breadth-first flood solves it.

Usage: python maze.py [--cols C] [--rows R] [--fps F] [--frames N] [--seed S] [--algo dfs|prim]
                      [--loops] [--no-color]
The carving head is bright, the BFS wavefront ripples out from the entrance, and the
shortest path is traced back in gold. Then a new maze begins.
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from collections.abc import Iterator

WALL, OPEN = 0, 1
Cell = tuple[int, int]


def carve_dfs(grid: list[list[int]], rng: random.Random) -> Iterator[Cell]:
    """Recursive backtracker on the odd-coordinate lattice; yields each newly opened cell."""
    h, w = len(grid), len(grid[0])
    start = (1, 1)
    grid[1][1] = OPEN
    stack = [start]
    yield start
    while stack:
        x, y = stack[-1]
        options = [(dx, dy) for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2))
                   if 0 < x + dx < w - 1 and 0 < y + dy < h - 1 and grid[y + dy][x + dx] == WALL]
        if not options:
            stack.pop()
            continue
        dx, dy = rng.choice(options)
        grid[y + dy // 2][x + dx // 2] = OPEN
        grid[y + dy][x + dx] = OPEN
        stack.append((x + dx, y + dy))
        yield (x + dx // 2, y + dy // 2)
        yield (x + dx, y + dy)


def carve_prim(grid: list[list[int]], rng: random.Random) -> Iterator[Cell]:
    """Randomised Prim's algorithm: grow from a frontier of walls (bushier, shorter dead ends)."""
    h, w = len(grid), len(grid[0])
    grid[1][1] = OPEN
    yield (1, 1)
    frontier = [(1, 1, dx, dy) for dx, dy in ((2, 0), (0, 2))]
    while frontier:
        x, y, dx, dy = frontier.pop(rng.randrange(len(frontier)))
        nx, ny = x + dx, y + dy
        if not (0 < nx < w - 1 and 0 < ny < h - 1) or grid[ny][nx] == OPEN:
            continue
        grid[y + dy // 2][x + dx // 2] = OPEN
        grid[ny][nx] = OPEN
        yield (x + dx // 2, y + dy // 2)
        yield (nx, ny)
        frontier += [(nx, ny, ex, ey) for ex, ey in ((2, 0), (-2, 0), (0, 2), (0, -2))]


def add_loops(grid: list[list[int]], rng: random.Random, fraction: float = 0.06) -> None:
    """Knock out a few interior walls so the maze has cycles (several routes)."""
    h, w = len(grid), len(grid[0])
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if grid[y][x] == WALL and (x + y) % 2 == 1 and rng.random() < fraction:
                if (grid[y][x - 1] == grid[y][x + 1] == OPEN) or (grid[y - 1][x] == grid[y + 1][x] == OPEN):
                    grid[y][x] = OPEN


def solve_bfs(grid: list[list[int]], start: Cell, goal: Cell) -> Iterator[tuple[list[Cell], dict[Cell, Cell | None]]]:
    """Breadth-first search; yields each wavefront layer and the parent links so far."""
    parent: dict[Cell, Cell | None] = {start: None}
    layer = [start]
    while layer:
        yield layer, parent
        if goal in parent:
            return
        nxt = []
        for x, y in layer:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if 0 <= n[1] < len(grid) and 0 <= n[0] < len(grid[0]) and grid[n[1]][n[0]] == OPEN \
                        and n not in parent:
                    parent[n] = (x, y)
                    nxt.append(n)
        layer = nxt


def path_to(parent: dict[Cell, Cell | None], goal: Cell) -> list[Cell]:
    """Follow parent links back from `goal`."""
    out: list[Cell] = []
    cur: Cell | None = goal if goal in parent else None
    while cur is not None:
        out.append(cur)
        cur = parent[cur]
    return out[::-1]


def render(grid: list[list[int]], paint: dict[Cell, str], color: bool) -> str:
    """Two characters per cell so the maze looks square."""
    lines = []
    for y, row in enumerate(grid):
        parts = []
        for x, v in enumerate(row):
            p = paint.get((x, y))
            if v == WALL:
                parts.append("\x1b[38;5;60m██" if color else "██")
            elif p and color:
                parts.append(f"{p}██")
            elif p:
                parts.append({"head": "@@", "wave": "::", "seen": "..", "path": "<>"}.get(p, "  "))
            else:
                parts.append("  ")
        lines.append("".join(parts) + ("\x1b[0m" if color else ""))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cols", type=int, default=17, help="maze cells across")
    ap.add_argument("--rows", type=int, default=10, help="maze cells down")
    ap.add_argument("--fps", type=float, default=60)
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--algo", choices=["dfs", "prim"], default="dfs")
    ap.add_argument("--loops", action="store_true", help="add a few cycles")
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    color = not a.no_color
    w, h = 2 * a.cols + 1, 2 * a.rows + 1
    C = {"head": "\x1b[38;5;231m", "fresh": "\x1b[38;5;24m", "wave": "\x1b[38;5;45m",
         "seen": "\x1b[38;5;23m", "path": "\x1b[38;5;220m"} if color else \
        {"head": "head", "fresh": "", "wave": "wave", "seen": "seen", "path": "path"}
    frame = 0

    def show(grid, paint, status):
        nonlocal frame
        sys.stdout.write("\x1b[H" + render(grid, paint, color) + f"\n{status}\x1b[K")
        sys.stdout.flush()
        frame += 1
        if a.frames and frame >= a.frames:
            raise StopIteration
        time.sleep(1 / a.fps)

    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while True:
            grid = [[WALL] * w for _ in range(h)]
            carve = carve_dfs if a.algo == "dfs" else carve_prim
            opened = 0
            for cell in carve(grid, rng):
                opened += 1
                if opened % 2 == 0:
                    show(grid, {cell: C["head"]}, f"carving ({a.algo})… {opened} cells")
            if a.loops:
                add_loops(grid, rng)
            start, goal = (1, 1), (w - 2, h - 2)
            grid[1][0] = grid[h - 2][w - 1] = OPEN  # entrance and exit
            paint: dict[Cell, str] = {}
            parent: dict[Cell, Cell | None] = {}
            for layer, parent in solve_bfs(grid, start, goal):
                for c in paint:
                    paint[c] = C["seen"]
                for c in layer:
                    paint[c] = C["wave"]
                show(grid, paint, f"breadth-first search: {len(parent)} cells reached")
            route = path_to(parent, goal)
            for i in range(1, len(route) + 1):
                for c in route[:i]:
                    paint[c] = C["path"]
                if i % 2 == 0 or i == len(route):
                    show(grid, paint, f"shortest path: {i}/{len(route)} steps")
            for _ in range(int(a.fps)):
                show(grid, paint, f"solved — shortest path {len(route)} steps, explored {len(parent)} cells")
    except (KeyboardInterrupt, StopIteration):
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")


if __name__ == "__main__":
    main()
