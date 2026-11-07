"""Knight's tour on an N×N board using Warnsdorff's rule (with tie-breaking lookahead).

Run: python knights_tour.py [N] [start_col start_row]   (default 8, from a1)
"""
from __future__ import annotations

import sys

JUMPS = ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2))


def tour(n: int, start: tuple[int, int] = (0, 0)) -> list[tuple[int, int]] | None:
    board = [[0] * n for _ in range(n)]

    def free(x, y):
        return 0 <= x < n and 0 <= y < n and board[y][x] == 0

    def degree(x, y):
        return sum(free(x + dx, y + dy) for dx, dy in JUMPS)

    x, y = start
    board[y][x] = 1
    path = [start]
    for step in range(2, n * n + 1):
        options = [(x + dx, y + dy) for dx, dy in JUMPS if free(x + dx, y + dy)]
        if not options:
            return None
        # fewest onward moves; break ties by the sum of the next squares' degrees
        x, y = min(options, key=lambda p: (degree(*p),
                                           sum(degree(p[0] + a, p[1] + b) for a, b in JUMPS if free(p[0] + a, p[1] + b))))
        board[y][x] = step
        path.append((x, y))
    return path


def is_valid(path: list[tuple[int, int]], n: int) -> bool:
    if len(set(path)) != n * n:
        return False
    return all((abs(a[0] - b[0]), abs(a[1] - b[1])) in ((1, 2), (2, 1)) for a, b in zip(path, path[1:]))


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    start = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 0)
    path = tour(n, start)
    if not path:
        print("Warnsdorff got stuck — try another start square.")
    else:
        order = {p: i + 1 for i, p in enumerate(path)}
        width = len(str(n * n))
        for y in range(n):
            print(" ".join(f"{order[(x, y)]:>{width}}" for x in range(n)))
        print("\nvalid:", is_valid(path, n))
