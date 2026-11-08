"""Line diff with the Myers O(ND) algorithm, printed as a coloured unified diff.

    python linediff.py old.txt new.txt          # unified diff, 3 lines of context
    python linediff.py -U 1 old.txt new.txt     # less context
    python linediff.py --demo                   # diff two built-in snippets

No difflib: the shortest edit script is found with Myers' greedy algorithm and then
grouped into hunks. Exit status is 0 when the files are equal and 1 otherwise (like diff).
"""
from __future__ import annotations

import sys
from typing import Sequence

GREEN, RED, CYAN, RESET = "\033[32m", "\033[31m", "\033[36m", "\033[0m"


def myers(a: Sequence[str], b: Sequence[str]) -> list[tuple[str, int, int]]:
    """Shortest edit script as ops (``=``, ``-``, ``+``) with indexes into ``a`` and ``b``."""
    n, m = len(a), len(b)
    maxd = n + m
    v = {1: 0}
    trace: list[dict[int, int]] = []
    for d in range(maxd + 1):
        trace.append(dict(v))
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v[k - 1] < v[k + 1]):
                x = v[k + 1]          # step down: insertion
            else:
                x = v[k - 1] + 1      # step right: deletion
            y = x - k
            while x < n and y < m and a[x] == b[y]:
                x, y = x + 1, y + 1
            v[k] = x
            if x >= n and y >= m:
                return _backtrack(trace, a, b, d)
    return []  # pragma: no cover - unreachable


def _backtrack(trace: list[dict[int, int]], a: Sequence[str], b: Sequence[str], dmax: int) -> list[tuple[str, int, int]]:
    x, y = len(a), len(b)
    ops: list[tuple[str, int, int]] = []
    for d in range(dmax, -1, -1):
        v = trace[d]
        k = x - y
        if d == 0:
            prev_k = 0
        elif k == -d or (k != d and v[k - 1] < v[k + 1]):
            prev_k = k + 1
        else:
            prev_k = k - 1
        prev_x = v[prev_k] if d else 0
        prev_y = prev_x - prev_k
        while x > prev_x and y > prev_y:
            x, y = x - 1, y - 1
            ops.append(("=", x, y))
        if d:
            if x == prev_x:
                ops.append(("+", x, prev_y))
            else:
                ops.append(("-", prev_x, y))
        x, y = prev_x, prev_y
    ops.reverse()
    return ops


def hunks(ops: list[tuple[str, int, int]], context: int = 3) -> list[list[tuple[str, int, int]]]:
    """Group edit ops into hunks with ``context`` unchanged lines around each change."""
    changes = [i for i, op in enumerate(ops) if op[0] != "="]
    if not changes:
        return []
    groups: list[list[int]] = [[changes[0]]]
    for i in changes[1:]:
        if i - groups[-1][-1] <= 2 * context + 1:
            groups[-1].append(i)
        else:
            groups.append([i])
    return [ops[max(0, g[0] - context): g[-1] + context + 1] for g in groups]


def unified(a: list[str], b: list[str], context: int = 3, color: bool = False,
            names: tuple[str, str] = ("a", "b")) -> list[str]:
    ops = myers(a, b)
    out: list[str] = []
    hs = hunks(ops, context)
    if not hs:
        return out
    c = (lambda code, s: f"{code}{s}{RESET}") if color else (lambda code, s: s)
    out += [c(RED, f"--- {names[0]}"), c(GREEN, f"+++ {names[1]}")]
    for h in hs:
        a_start = next((i for op, i, _ in h if op in "=-"), h[0][1])
        b_start = next((j for op, _, j in h if op in "=+"), h[0][2])
        a_len = sum(1 for op, _, _ in h if op in "=-")
        b_len = sum(1 for op, _, _ in h if op in "=+")
        out.append(c(CYAN, f"@@ -{a_start + 1},{a_len} +{b_start + 1},{b_len} @@"))
        for op, i, j in h:
            if op == "=":
                out.append(" " + a[i])
            elif op == "-":
                out.append(c(RED, "-" + a[i]))
            else:
                out.append(c(GREEN, "+" + b[j]))
    return out


DEMO_A = """def greet(name):
    print("Hello", name)

def main():
    greet("world")
    greet("moon")
""".splitlines()
DEMO_B = """def greet(name, punct="!"):
    print("Hello", name + punct)

def main():
    greet("world")
    greet("sun")
    greet("moon")
""".splitlines()


def main(argv: list[str]) -> int:
    context = 3
    if "-U" in argv:
        i = argv.index("-U")
        context = int(argv[i + 1])
        del argv[i: i + 2]
    color = sys.stdout.isatty()
    if argv == ["--demo"] or not argv:
        a, b, names = DEMO_A, DEMO_B, ("demo/old.py", "demo/new.py")
    elif len(argv) == 2:
        with open(argv[0], encoding="utf-8", errors="replace") as fa, \
                open(argv[1], encoding="utf-8", errors="replace") as fb:
            a, b = fa.read().splitlines(), fb.read().splitlines()
        names = (argv[0], argv[1])
    else:
        print(__doc__)
        return 2
    lines = unified(a, b, context, color, names)
    print("\n".join(lines))
    return 1 if lines else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
