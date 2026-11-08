"""English peg solitaire solver (33-hole cross board, finish with one peg in the centre).

Depth-first search over moves with memoisation of dead positions, using the board's 8-fold
symmetry to recognise positions already proven hopeless. Solves the classic board in well
under a second and replays the 31 jumps.

Run: python peg_solitaire.py [--quiet]
"""
from __future__ import annotations

import sys

LAYOUT = [
    "  ooo  ",
    "  ooo  ",
    "ooooooo",
    "ooo.ooo",
    "ooooooo",
    "  ooo  ",
    "  ooo  ",
]
HOLES = [(x, y) for y, row in enumerate(LAYOUT) for x, ch in enumerate(row) if ch != " "]
INDEX = {p: i for i, p in enumerate(HOLES)}
CENTRE = INDEX[(3, 3)]


def _moves() -> list[tuple[int, int, int]]:
    """Every (from, over, to) jump on the board."""
    out = []
    for (x, y) in HOLES:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            over, to = (x + dx, y + dy), (x + 2 * dx, y + 2 * dy)
            if over in INDEX and to in INDEX:
                out.append((INDEX[(x, y)], INDEX[over], INDEX[to]))
    return out


MOVES = _moves()


def _symmetries() -> list[list[int]]:
    maps = []
    for t in range(8):
        perm = []
        for (x, y) in HOLES:
            cx, cy = x - 3, y - 3
            for _ in range(t % 4):
                cx, cy = -cy, cx
            if t >= 4:
                cx = -cx
            perm.append(INDEX[(cx + 3, cy + 3)])
        maps.append(perm)
    return maps


SYMS = _symmetries()


def canonical(board: int) -> int:
    best = None
    for perm in SYMS:
        b = 0
        for i, j in enumerate(perm):
            if board >> i & 1:
                b |= 1 << j
        if best is None or b < best:
            best = b
    return best


def solve(start: int, goal: int) -> list[tuple[int, int, int]] | None:
    dead: set[int] = set()
    path: list[tuple[int, int, int]] = []

    def dfs(board: int) -> bool:
        if board == goal:
            return True
        key = canonical(board)
        if key in dead:
            return False
        for f, o, t in MOVES:
            if board >> f & 1 and board >> o & 1 and not board >> t & 1:
                path.append((f, o, t))
                if dfs(board ^ (1 << f) ^ (1 << o) ^ (1 << t)):
                    return True
                path.pop()
        dead.add(key)
        return False

    return list(path) if dfs(start) else None


def draw(board: int) -> str:
    rows = []
    for y, row in enumerate(LAYOUT):
        line = ""
        for x, ch in enumerate(row):
            line += "  " if ch == " " else ("● " if board >> INDEX[(x, y)] & 1 else "· ")
        rows.append(line.rstrip())
    return "\n".join(rows)


def main() -> None:
    quiet = "--quiet" in sys.argv
    full = (1 << len(HOLES)) - 1
    start, goal = full ^ (1 << CENTRE), 1 << CENTRE
    path = solve(start, goal)
    if path is None:
        print("no solution")
        return
    board = start
    print(draw(board))
    for n, (f, o, t) in enumerate(path, 1):
        board ^= (1 << f) | (1 << o) | (1 << t)
        if not quiet:
            print(f"\nmove {n}: {HOLES[f]} jumps {HOLES[o]} -> {HOLES[t]}")
            print(draw(board))
    print(f"\nSolved in {len(path)} jumps: one peg left in the centre.")


if __name__ == "__main__":
    main()
