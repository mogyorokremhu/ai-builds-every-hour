"""Nonogram (picross) solver using line-by-line constraint propagation + backtracking.

Run: python nonogram.py    (solves a built-in picture)
"""
from __future__ import annotations

from functools import lru_cache

# A little house picture. Only its clues are handed to the solver.
PICTURE = """
...#...
..###..
.#####.
#######
.#...#.
.#.#.#.
.#.#.#.
.#####.
"""


def clues_of(lines: list[str]) -> list[list[int]]:
    """Run lengths of '#' in each line, e.g. '.##.#' -> [2, 1]."""
    return [[len(run) for run in line.split(".") if run] for line in lines]


_ROWS_TXT = PICTURE.strip().splitlines()
ROWS = clues_of(_ROWS_TXT)
COLS = clues_of(["".join(r[c] for r in _ROWS_TXT) for c in range(len(_ROWS_TXT[0]))])


@lru_cache(maxsize=None)
def arrangements(clue: tuple[int, ...], length: int) -> tuple[tuple[int, ...], ...]:
    """Every way to place the clue's runs in a line of ``length`` cells (1 = filled)."""
    if not clue:
        return ((0,) * length,)
    first, rest = clue[0], clue[1:]
    min_rest = sum(rest) + len(rest)
    out = []
    for start in range(length - min_rest - first + 1):
        head = (0,) * start + (1,) * first
        if rest:
            head += (0,)
        for tail in arrangements(rest, length - len(head)):
            out.append(head + tail)
    return tuple(out)


def fits(line: tuple[int, ...], known: list[int | None]) -> bool:
    return all(k is None or k == v for v, k in zip(line, known))


def propagate(grid, rows, cols) -> bool:
    """Fix cells that every remaining arrangement agrees on. False on contradiction."""
    changed = True
    h, w = len(rows), len(cols)
    while changed:
        changed = False
        for lines, get, put, count in (
            (rows, lambda i: grid[i], lambda i, j, v: grid[i].__setitem__(j, v), h),
            (cols, lambda j: [grid[i][j] for i in range(h)], lambda j, i, v: grid[i].__setitem__(j, v), w),
        ):
            for idx in range(count):
                known = get(idx)
                if None not in known:
                    continue
                options = [a for a in arrangements(tuple(lines[idx]), len(known)) if fits(a, known)]
                if not options:
                    return False
                for pos in range(len(known)):
                    if known[pos] is None:
                        vals = {o[pos] for o in options}
                        if len(vals) == 1:
                            put(idx, pos, vals.pop())
                            changed = True
    return True


def solve(rows, cols):
    grid: list[list[int | None]] = [[None] * len(cols) for _ in rows]

    def rec(g):
        if not propagate(g, rows, cols):
            return None
        for i, row in enumerate(g):
            for j, v in enumerate(row):
                if v is None:
                    for guess in (1, 0):
                        trial = [r[:] for r in g]
                        trial[i][j] = guess
                        res = rec(trial)
                        if res:
                            return res
                    return None
        return g

    return rec(grid)


if __name__ == "__main__":
    result = solve(ROWS, COLS)
    if result is None:
        print("No solution.")
    else:
        for clue, row in zip(ROWS, result):
            print("".join("██" if v else "··" for v in row), " ", *clue)
        print("matches picture:", ["".join("#" if v else "." for v in r) for r in result] == _ROWS_TXT)
