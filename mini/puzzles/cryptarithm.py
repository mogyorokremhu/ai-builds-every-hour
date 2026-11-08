"""Cryptarithm solver: SEND + MORE = MONEY and friends.

Each letter stands for a different digit and no number starts with 0. The solver builds a
weighted sum (every letter's place values across the equation) and runs a backtracking
search, assigning the letters with the largest weights first and pruning with bounds on
what the remaining letters could still contribute.

Run: python cryptarithm.py "SEND + MORE = MONEY"
     python cryptarithm.py "TWO + TWO = FOUR"      (supports + and - and several terms)
"""
from __future__ import annotations

import re
import sys


def parse(puzzle: str) -> tuple[dict[str, int], set[str]]:
    """Return letter weights (left side positive, right negative) and leading letters."""
    left, right = puzzle.replace(" ", "").upper().split("=")
    weights: dict[str, int] = {}
    leading: set[str] = set()

    def add_side(side: str, sign: int) -> None:
        for op, word in re.findall(r"([+-]?)([A-Z]+)", side):
            s = sign * (-1 if op == "-" else 1)
            if len(word) > 1:
                leading.add(word[0])
            for i, ch in enumerate(reversed(word)):
                weights[ch] = weights.get(ch, 0) + s * 10 ** i

    add_side(left, 1)
    add_side(right, -1)
    if len(weights) > 10:
        raise ValueError("more than 10 distinct letters")
    return weights, leading


def solve(puzzle: str) -> list[dict[str, int]]:
    weights, leading = parse(puzzle)
    letters = sorted(weights, key=lambda c: -abs(weights[c]))
    ws = [weights[c] for c in letters]
    solutions: list[dict[str, int]] = []
    assign = [0] * len(letters)
    used = [False] * 10

    def bounds(i: int) -> tuple[int, int]:
        """Loose min/max of the remaining weighted sum (digits 0-9, ignoring distinctness)."""
        lo = sum(min(0, w * 9) for w in ws[i:])
        hi = sum(max(0, w * 9) for w in ws[i:])
        return lo, hi

    rest = [bounds(i) for i in range(len(letters) + 1)]

    def go(i: int, total: int) -> None:
        if i == len(letters):
            if total == 0:
                solutions.append(dict(zip(letters, assign)))
            return
        lo, hi = rest[i]
        if total + lo > 0 or total + hi < 0:
            return
        for d in range(10):
            if used[d] or (d == 0 and letters[i] in leading):
                continue
            used[d] = True
            assign[i] = d
            go(i + 1, total + ws[i] * d)
            used[d] = False

    go(0, 0)
    return solutions


def render(puzzle: str, sol: dict[str, int]) -> str:
    return "".join(str(sol[ch]) if ch in sol else ch for ch in puzzle.upper())


def main() -> None:
    puzzle = sys.argv[1] if len(sys.argv) > 1 else "SEND + MORE = MONEY"
    sols = solve(puzzle)
    print(puzzle)
    if not sols:
        print("no solution")
    for s in sols[:10]:
        print("  " + render(puzzle, s) + "   " + " ".join(f"{k}={v}" for k, v in sorted(s.items())))
    if len(sols) > 10:
        print(f"  ... {len(sols)} solutions in total")


if __name__ == "__main__":
    main()
