"""N-Queens: count all solutions with bitmasks and draw the first one.

Run: python n_queens.py [N]   (default 8)
"""
from __future__ import annotations

import sys


def solutions(n: int):
    """Yield each solution as a list of column indices (one per row)."""
    full = (1 << n) - 1
    cols: list[int] = []

    def place(row: int, used: int, d1: int, d2: int):
        if row == n:
            yield cols[:]
            return
        free = full & ~(used | d1 | d2)
        while free:
            bit = free & -free
            free ^= bit
            cols.append(bit.bit_length() - 1)
            yield from place(row + 1, used | bit, (d1 | bit) << 1 & full, (d2 | bit) >> 1)
            cols.pop()

    yield from place(0, 0, 0, 0)


def count(n: int) -> int:
    return sum(1 for _ in solutions(n))


def draw(cols: list[int]) -> str:
    n = len(cols)
    return "\n".join(" ".join("♛" if c == q else ("·" if (r + c) % 2 else "□") for c in range(n))
                     for r, q in enumerate(cols))


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    first = next(solutions(n), None)
    if first is None:
        print(f"No solution for N={n}.")
    else:
        print(draw(first))
        print(f"\n{count(n)} solutions for N={n}.")
