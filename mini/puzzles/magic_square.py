"""Magic squares of any order n >= 3 (every row, column and diagonal has the same sum).

Three classic constructions:

* odd n           — the Siamese method (move up-right, drop down when blocked);
* doubly even n   — fill 1..n² and complement the cells on the "X" pattern of 4x4 blocks;
* singly even n   — LUX/Strachey: four odd magic squares in quadrants plus column swaps.

Run: python magic_square.py [n]   (default: shows 3, 4, 5 and 6)
"""
from __future__ import annotations

import sys


def odd(n: int) -> list[list[int]]:
    sq = [[0] * n for _ in range(n)]
    x, y = n // 2, 0
    for k in range(1, n * n + 1):
        sq[y][x] = k
        nx, ny = (x + 1) % n, (y - 1) % n
        if sq[ny][nx]:
            nx, ny = x, (y + 1) % n
        x, y = nx, ny
    return sq


def doubly_even(n: int) -> list[list[int]]:
    sq = [[y * n + x + 1 for x in range(n)] for y in range(n)]
    for y in range(n):
        for x in range(n):
            if (x % 4 in (0, 3)) == (y % 4 in (0, 3)):
                sq[y][x] = n * n + 1 - sq[y][x]
    return sq


def singly_even(n: int) -> list[list[int]]:
    """Strachey's method for n = 4k + 2."""
    h = n // 2
    sub = odd(h)
    # quadrants: A = top-left (+0), B = bottom-right (+h²), C = top-right (+2h²), D = bottom-left (+3h²)
    sq = [[0] * n for _ in range(n)]
    for y in range(h):
        for x in range(h):
            v = sub[y][x]
            sq[y][x] = v                             # A
            sq[y + h][x + h] = v + h * h             # B
            sq[y][x + h] = v + 2 * h * h             # C
            sq[y + h][x] = v + 3 * h * h             # D
    k = (n - 2) // 4
    for y in range(h):
        cols = list(range(k))
        if y == h // 2:
            cols = [c + 1 for c in cols]  # the middle row shifts one to the right
        for x in cols:
            sq[y][x], sq[y + h][x] = sq[y + h][x], sq[y][x]
        for x in range(n - k + 1, n):
            sq[y][x], sq[y + h][x] = sq[y + h][x], sq[y][x]
    return sq


def magic(n: int) -> list[list[int]]:
    if n < 3:
        raise ValueError("no magic squares of order 2 (order 1 is trivial)")
    if n % 2:
        return odd(n)
    if n % 4 == 0:
        return doubly_even(n)
    return singly_even(n)


def is_magic(sq: list[list[int]]) -> bool:
    n = len(sq)
    target = n * (n * n + 1) // 2
    lines = sq + [list(c) for c in zip(*sq)]
    lines += [[sq[i][i] for i in range(n)], [sq[i][n - 1 - i] for i in range(n)]]
    return all(sum(line) == target for line in lines) and sorted(v for r in sq for v in r) == list(
        range(1, n * n + 1))


def show(sq: list[list[int]]) -> str:
    w = len(str(len(sq) ** 2))
    return "\n".join(" ".join(f"{v:>{w}}" for v in row) for row in sq)


def main() -> None:
    orders = [int(sys.argv[1])] if len(sys.argv) > 1 else [3, 4, 5, 6]
    for n in orders:
        sq = magic(n)
        print(f"order {n}, magic sum {n * (n * n + 1) // 2}, valid: {is_magic(sq)}")
        print(show(sq) + "\n")


if __name__ == "__main__":
    main()
