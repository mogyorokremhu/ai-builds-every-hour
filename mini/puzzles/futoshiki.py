#!/usr/bin/env python3
"""Futoshiki ("inequality") puzzle solver with arc consistency.

Fill an N×N grid with 1..N, once per row and column, so that every < / > sign between
neighbouring cells holds. The solver keeps a candidate set per cell, runs AC-3 style
propagation (all-different + inequalities, including "a > b" ⇒ a ≥ 2, b ≤ N-1 and
bounds that flow along chains), then backtracks on the cell with fewest candidates.

    python futoshiki.py          # solve the built-in 5×5 puzzle
    python futoshiki.py --steps  # also report how many guesses were needed

Puzzle format: rows of cells ('.' or a digit) with signs between them; the lines in
between hold '^' (upper < lower) or 'v' (upper > lower) under the cells they join.
"""
from __future__ import annotations

import sys

PUZZLE = """\
. . . . .
v        
. . .<. .
      ^  
. . . . .
  ^     v
.>. . . 1
      v  
. . 3 . .
"""


def parse(text: str):
    """Return (n, givens {(r,c): v}, relations [((r1,c1),(r2,c2))] meaning cell1 < cell2)."""
    lines = text.rstrip("\n").split("\n")
    cell_lines = lines[0::2]
    gap_lines = lines[1::2]
    n = len(cell_lines)
    givens, less = {}, []
    for r, line in enumerate(cell_lines):
        line = line.ljust(2 * n - 1)
        for c in range(n):
            ch = line[2 * c]
            if ch.isdigit():
                givens[(r, c)] = int(ch)
            if c < n - 1:
                sign = line[2 * c + 1]
                if sign == "<":
                    less.append(((r, c), (r, c + 1)))
                elif sign == ">":
                    less.append(((r, c + 1), (r, c)))
    for r, line in enumerate(gap_lines):
        line = line.ljust(2 * n - 1)
        for c in range(n):
            sign = line[2 * c]
            if sign == "^":
                less.append(((r, c), (r + 1, c)))
            elif sign == "v":
                less.append(((r + 1, c), (r, c)))
    return n, givens, less


class Solver:
    def __init__(self, n: int, givens, less):
        self.n = n
        self.less = less
        self.guesses = 0
        self.dom = {(r, c): set(range(1, n + 1)) for r in range(n) for c in range(n)}
        for cell, v in givens.items():
            self.dom[cell] = {v}

    def peers(self, cell):
        r, c = cell
        return [(r, k) for k in range(self.n) if k != c] + [(k, c) for k in range(self.n) if k != r]

    def propagate(self, dom) -> bool:
        changed = True
        while changed:
            changed = False
            for cell, d in dom.items():
                if not d:
                    return False
                if len(d) == 1:
                    v = next(iter(d))
                    for p in self.peers(cell):
                        if v in dom[p]:
                            dom[p] = dom[p] - {v}
                            changed = True
                            if not dom[p]:
                                return False
            for a, b in self.less:
                hi = max(dom[b])
                lo = min(dom[a])
                na = {v for v in dom[a] if v < hi}
                nb = {v for v in dom[b] if v > lo}
                if na != dom[a] or nb != dom[b]:
                    dom[a], dom[b] = na, nb
                    changed = True
                    if not na or not nb:
                        return False
            # hidden singles: a value with only one place left in a row/column
            for i in range(self.n):
                for line in ([(i, k) for k in range(self.n)], [(k, i) for k in range(self.n)]):
                    for v in range(1, self.n + 1):
                        spots = [c for c in line if v in dom[c]]
                        if not spots:
                            return False
                        if len(spots) == 1 and len(dom[spots[0]]) > 1:
                            dom[spots[0]] = {v}
                            changed = True
        return True

    def solve(self, dom=None):
        dom = {k: set(v) for k, v in (dom or self.dom).items()}
        if not self.propagate(dom):
            return None
        open_cells = [c for c, d in dom.items() if len(d) > 1]
        if not open_cells:
            return dom
        cell = min(open_cells, key=lambda c: len(dom[c]))
        for v in sorted(dom[cell]):
            self.guesses += 1
            trial = {k: set(d) for k, d in dom.items()}
            trial[cell] = {v}
            res = self.solve(trial)
            if res:
                return res
        return None


def render(n, dom, less) -> str:
    rel = set(less)
    out = []
    for r in range(n):
        row = ""
        for c in range(n):
            row += str(next(iter(dom[(r, c)])))
            if c < n - 1:
                row += "<" if ((r, c), (r, c + 1)) in rel else ">" if ((r, c + 1), (r, c)) in rel else " "
        out.append(row)
        if r < n - 1:
            gap = ""
            for c in range(n):
                gap += "^" if ((r, c), (r + 1, c)) in rel else "v" if ((r + 1, c), (r, c)) in rel else " "
                if c < n - 1:
                    gap += " "
            out.append(gap)
    return "\n".join(out)


def check(n, dom, less) -> bool:
    g = {k: next(iter(v)) for k, v in dom.items()}
    rows_ok = all(len({g[(r, c)] for c in range(n)}) == n for r in range(n))
    cols_ok = all(len({g[(r, c)] for r in range(n)}) == n for c in range(n))
    return rows_ok and cols_ok and all(g[a] < g[b] for a, b in less)


def main() -> None:
    n, givens, less = parse(PUZZLE)
    print("Puzzle:\n" + PUZZLE)
    s = Solver(n, givens, less)
    sol = s.solve()
    if not sol:
        print("No solution.")
        return
    print("Solution:\n" + render(n, sol, less))
    assert check(n, sol, less)
    if "--steps" in sys.argv:
        print(f"\n{s.guesses} guess(es) after propagation.")


if __name__ == "__main__":
    main()
