"""Lights Out solver: Gaussian elimination over GF(2).

Pressing a light toggles it and its four neighbours. Every press is its own inverse, so a
solution is a set of presses x with A·x = b (mod 2), where A is the toggle matrix and b
the lit cells. We solve it with bitmask row reduction and pick the solution with the
fewest presses among the null-space combinations.

Run: python lights_out.py [size] [seed]    (default 5x5, random puzzle)
"""
from __future__ import annotations

import random
import sys


def toggle_masks(n: int) -> list[int]:
    """Bitmask of cells toggled by pressing each cell of an n x n board."""
    masks = []
    for y in range(n):
        for x in range(n):
            m = 0
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    m |= 1 << (ny * n + nx)
            masks.append(m)
    return masks


def solve(board: int, n: int) -> list[int] | None:
    """Return the cells to press (indices) to switch every light off, or None if impossible."""
    cells = n * n
    masks = toggle_masks(n)
    # augmented rows: row i = which presses affect cell i, plus the target bit
    rows = []
    for i in range(cells):
        r = 0
        for j, m in enumerate(masks):
            if m >> i & 1:
                r |= 1 << j
        rows.append(r | ((board >> i & 1) << cells))
    pivots: list[int] = []
    r = 0
    for col in range(cells):
        pivot = next((k for k in range(r, cells) if rows[k] >> col & 1), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        for k in range(cells):
            if k != r and rows[k] >> col & 1:
                rows[k] ^= rows[r]
        pivots.append(col)
        r += 1
    if any(rows[k] >> cells & 1 for k in range(r, cells)):
        return None  # inconsistent
    free = [c for c in range(cells) if c not in pivots]
    best = None
    for combo in range(1 << len(free)):
        x = 0
        for i, c in enumerate(free):
            if combo >> i & 1:
                x |= 1 << c
        for k, col in enumerate(pivots):
            row = rows[k]
            bit = row >> cells & 1
            for c in free:
                if row >> c & 1 and x >> c & 1:
                    bit ^= 1
            if bit:
                x |= 1 << col
        if best is None or bin(x).count("1") < bin(best).count("1"):
            best = x
    return [i for i in range(cells) if best >> i & 1]


def press(board: int, n: int, cell: int) -> int:
    return board ^ toggle_masks(n)[cell]


def show(board: int, n: int, marks: set[int] = frozenset()) -> str:
    out = []
    for y in range(n):
        row = ""
        for x in range(n):
            i = y * n + x
            ch = "●" if board >> i & 1 else "·"
            row += f"[{ch}]" if i in marks else f" {ch} "
        out.append(row)
    return "\n".join(out)


def random_puzzle(n: int, rng: random.Random) -> int:
    """Generate a solvable board by pressing random cells on a dark board."""
    board = 0
    for cell in range(n * n):
        if rng.random() < 0.5:
            board = press(board, n, cell)
    return board


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else random.randrange(10**6)
    board = random_puzzle(n, random.Random(seed))
    presses = solve(board, n)
    print(f"Lights Out {n}x{n} (seed {seed}) — [x] marks a press in the solution\n")
    print(show(board, n, set(presses or [])))
    if presses is None:
        print("\nNo solution.")
        return
    for cell in presses:
        board = press(board, n, cell)
    print(f"\n{len(presses)} presses; board after solving:\n")
    print(show(board, n))
    assert board == 0


if __name__ == "__main__":
    main()
