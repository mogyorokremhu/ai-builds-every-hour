"""Solve an ASCII maze with BFS (shortest path) and draw the route with '.'."""
import random
import sys
from collections import deque

from recursive_backtracker import generate


def solve(rows: list[str]) -> list[str] | None:
    """Path from top-left cell to bottom-right cell, or None if unreachable."""
    h, w = len(rows), len(rows[0])
    start, goal = (1, 1), (w - 2, h - 2)
    prev = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == goal:
            break
        x, y = cur
        for nxt in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if nxt not in prev and rows[nxt[1]][nxt[0]] == " ":
                prev[nxt] = cur
                q.append(nxt)
    if goal not in prev:
        return None
    grid = [list(r) for r in rows]
    cur = goal
    while cur:
        grid[cur[1]][cur[0]] = "."
        cur = prev[cur]
    return ["".join(r) for r in grid]


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else None
    maze = generate(12, 6, random.Random(seed))
    print("\n".join(solve(maze) or maze))
