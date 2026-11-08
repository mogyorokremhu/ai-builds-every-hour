#!/usr/bin/env python3
"""Klotski (the "Forget-me-not" sliding block puzzle) solved optimally with BFS.

The classic 4x5 board: move the big 2x2 block to the exit at the bottom middle.
States are canonicalised by block *shape* (identical pieces are interchangeable),
which cuts the search space from millions to ~25,000 states. Every slide of one
block by one cell counts as a move; the classic layout needs 116 such moves.
(Merging a block's consecutive slides into one move gives a shorter count for
this path; the true minimum under that metric, 81, needs a different search.)

    python klotski.py            # solve the classic layout, print every 10th step
    python klotski.py --all      # print every step
"""
from __future__ import annotations

import sys
from collections import deque

W, H = 4, 5
# (width, height, col, row); the first block is the 2x2 that must escape
CLASSIC: list[tuple[int, int, int, int]] = [
    (2, 2, 1, 0),
    (1, 2, 0, 0), (1, 2, 3, 0), (1, 2, 0, 2), (1, 2, 3, 2),
    (2, 1, 1, 2),
    (1, 1, 1, 3), (1, 1, 2, 3), (1, 1, 0, 4), (1, 1, 3, 4),
]
GOAL = (1, 3)  # top-left corner of the big block when it can slide out

Block = tuple[int, int, int, int]
State = tuple[Block, ...]


def canonical(blocks: State) -> tuple:
    """Key that treats same-shaped blocks as identical (keeps the big block first)."""
    return (blocks[0], tuple(sorted(blocks[1:])))


def occupied(blocks: State) -> set[tuple[int, int]]:
    cells: set[tuple[int, int]] = set()
    for w, h, c, r in blocks:
        for dx in range(w):
            for dy in range(h):
                cells.add((c + dx, r + dy))
    return cells


def moves(blocks: State):
    """Yield (block index, direction, new state) for every one-cell slide."""
    filled = occupied(blocks)
    for i, (w, h, c, r) in enumerate(blocks):
        own = {(c + dx, r + dy) for dx in range(w) for dy in range(h)}
        others = filled - own
        for name, (mx, my) in (("left", (-1, 0)), ("right", (1, 0)), ("up", (0, -1)), ("down", (0, 1))):
            nc, nr = c + mx, r + my
            if nc < 0 or nr < 0 or nc + w > W or nr + h > H:
                continue
            new = {(nc + dx, nr + dy) for dx in range(w) for dy in range(h)}
            if new & others:
                continue
            nb = list(blocks)
            nb[i] = (w, h, nc, nr)
            yield i, name, tuple(nb)


def solve(start: State) -> list[tuple[int, str, State]]:
    """Shortest list of (block, direction, state after) slides that frees the big block."""
    key0 = canonical(start)
    prev: dict[tuple, tuple | None] = {key0: None}
    states = {key0: (start, None, None)}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if (cur[0][2], cur[0][3]) == GOAL:
            path = []
            k = canonical(cur)
            while prev[k] is not None:
                st, i, d = states[k]
                path.append((i, d, st))
                k = prev[k]
            return path[::-1]
        ck = canonical(cur)
        for i, d, nxt in moves(cur):
            nk = canonical(nxt)
            if nk in prev:
                continue
            prev[nk] = ck
            states[nk] = (nxt, i, d)
            queue.append(nxt)
    return []


def draw(blocks: State) -> str:
    grid = [["." for _ in range(W)] for _ in range(H)]
    for idx, (w, h, c, r) in enumerate(blocks):
        ch = "#" if idx == 0 else ("|" if h == 2 else "=" if w == 2 else "o")
        for dx in range(w):
            for dy in range(h):
                grid[r + dy][c + dx] = ch
    return "\n".join(" ".join(row) for row in grid)


def merged_moves(path: list[tuple[int, str, State]]) -> int:
    """Count moves when consecutive slides of the same block count once."""
    count, last = 0, None
    for i, d, st in path:
        pos = (st[i][2], st[i][3])
        if last is None or last[0] != i:
            count += 1
        last = (i, pos)
    return count


def main() -> None:
    every = 1 if "--all" in sys.argv else 10
    path = solve(tuple(CLASSIC))
    print("Start:\n" + draw(tuple(CLASSIC)) + "\n")
    for n, (i, d, st) in enumerate(path, 1):
        if n % every == 0 or n == len(path):
            print(f"Step {n}: block {i} {d}\n{draw(st)}\n")
    print(f"Solved in {len(path)} single-cell slides ({merged_moves(path)} block moves). The big block exits below.")


if __name__ == "__main__":
    main()
