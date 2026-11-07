"""Towers of Hanoi, animated in the terminal (iterative solution, 2^n - 1 moves).

Run: python hanoi.py [disks] [delay_seconds]   (default 5 disks, 0.25s)
"""
from __future__ import annotations

import sys
import time


def moves(n: int, src: int = 0, dst: int = 2, via: int = 1):
    """Yield (from_peg, to_peg) for the optimal solution."""
    if n == 0:
        return
    yield from moves(n - 1, src, via, dst)
    yield src, dst
    yield from moves(n - 1, via, dst, src)


def draw(pegs: list[list[int]], n: int) -> str:
    rows = []
    for level in range(n - 1, -1, -1):
        row = []
        for peg in pegs:
            if level < len(peg):
                d = peg[level]
                row.append(" " * (n - d) + "█" * (2 * d - 1) + " " * (n - d))
            else:
                row.append(" " * (n - 1) + "|" + " " * (n - 1))
        rows.append("  ".join(row))
    rows.append("=" * ((2 * n - 1) * 3 + 4))
    return "\n".join(rows)


def play(n: int, delay: float) -> int:
    pegs = [list(range(n, 0, -1)), [], []]
    count = 0
    print(draw(pegs, n))
    for a, b in moves(n):
        disk = pegs[a].pop()
        assert not pegs[b] or pegs[b][-1] > disk, "illegal move"
        pegs[b].append(disk)
        count += 1
        if delay:
            time.sleep(delay)
            print("\033[H\033[J", end="")
        print(f"move {count}: disk {disk} from {'ABC'[a]} to {'ABC'[b]}")
        print(draw(pegs, n))
    return count


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    delay = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25
    total = play(n, delay)
    print(f"\nSolved in {total} moves (2^{n} - 1 = {2 ** n - 1}).")
