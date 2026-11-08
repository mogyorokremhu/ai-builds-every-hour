#!/usr/bin/env python3
"""difftool — line diff with Myers' O(ND) algorithm, unified or side-by-side output.

Usage:
    python difftool.py OLD NEW [-u N] [--side] [--no-color] [-w]

* ``-u N``      lines of context around each change (default 3)
* ``--side``    side-by-side view (``|`` changed, ``<`` deleted, ``>`` added)
* ``-w``        ignore whitespace differences
* exit status   0 = identical, 1 = different (like ``diff``)

The diff itself is computed here from scratch (no ``difflib``): Myers' greedy algorithm
finds a shortest edit script by exploring diagonals of the edit graph, then the trace is
walked backwards to recover the edits.
"""
from __future__ import annotations

import shutil
import sys

RED, GREEN, CYAN, DIM, RESET = "\033[31m", "\033[32m", "\033[36m", "\033[2m", "\033[0m"


def myers(a: list[str], b: list[str]) -> list[tuple[str, int, int]]:
    """Shortest edit script as ('=', i, j) / ('-', i, -1) / ('+', -1, j) operations."""
    n, m = len(a), len(b)
    maxd = n + m
    v = {1: 0}
    trace: list[dict[int, int]] = []
    for d in range(maxd + 1):
        trace.append(dict(v))
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                x = v.get(k + 1, 0)          # move down (insertion)
            else:
                x = v.get(k - 1, 0) + 1      # move right (deletion)
            y = x - k
            while x < n and y < m and a[x] == b[y]:
                x, y = x + 1, y + 1
            v[k] = x
            if x >= n and y >= m:
                return _backtrack(trace, a, b, d)
    return []  # pragma: no cover


def _backtrack(trace, a, b, dmax) -> list[tuple[str, int, int]]:
    x, y = len(a), len(b)
    ops: list[tuple[str, int, int]] = []
    for d in range(dmax, -1, -1):
        v = trace[d]
        k = x - y
        if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
            prev_k = k + 1
        else:
            prev_k = k - 1
        prev_x = v.get(prev_k, 0)
        prev_y = prev_x - prev_k
        while x > prev_x and y > prev_y:
            x, y = x - 1, y - 1
            ops.append(("=", x, y))
        if d > 0:
            if x == prev_x:
                ops.append(("+", -1, prev_y))
            else:
                ops.append(("-", prev_x, -1))
        x, y = prev_x, prev_y
    ops.reverse()
    return ops


def hunks(ops, context: int = 3) -> list[list[tuple[str, int, int]]]:
    """Group operations into hunks with ``context`` unchanged lines around changes."""
    changed = [i for i, op in enumerate(ops) if op[0] != "="]
    if not changed:
        return []
    groups: list[list[int]] = [[changed[0]]]
    for i in changed[1:]:
        if i - groups[-1][-1] <= 2 * context + 1:
            groups[-1].append(i)
        else:
            groups.append([i])
    return [ops[max(0, g[0] - context): g[-1] + context + 1] for g in groups]


def unified(a, b, ops, context=3, color=True, names=("a", "b")) -> list[str]:
    paint = (lambda c, s: f"{c}{s}{RESET}") if color else (lambda c, s: s)
    out = [paint(DIM, f"--- {names[0]}"), paint(DIM, f"+++ {names[1]}")]
    for h in hunks(ops, context):
        a_lines = [op for op in h if op[0] != "+"]
        b_lines = [op for op in h if op[0] != "-"]
        a0 = next((op[1] for op in h if op[1] >= 0), 0)
        b0 = next((op[2] for op in h if op[2] >= 0), 0)
        out.append(paint(CYAN, f"@@ -{a0 + 1},{len(a_lines)} +{b0 + 1},{len(b_lines)} @@"))
        for kind, i, j in h:
            if kind == "=":
                out.append(" " + a[i])
            elif kind == "-":
                out.append(paint(RED, "-" + a[i]))
            else:
                out.append(paint(GREEN, "+" + b[j]))
    return out


def side_by_side(a, b, ops, width: int | None = None) -> list[str]:
    width = width or shutil.get_terminal_size((100, 20)).columns
    col = max(10, (width - 3) // 2)
    rows: list[tuple[str, str, str]] = []
    pend_del: list[str] = []
    pend_add: list[str] = []

    def flush() -> None:
        for k in range(max(len(pend_del), len(pend_add))):
            left = pend_del[k] if k < len(pend_del) else ""
            right = pend_add[k] if k < len(pend_add) else ""
            mark = "|" if k < len(pend_del) and k < len(pend_add) else "<" if k < len(pend_del) else ">"
            rows.append((left, mark, right))
        pend_del.clear()
        pend_add.clear()

    for kind, i, j in ops:
        if kind == "=":
            flush()
            rows.append((a[i], " ", b[j]))
        elif kind == "-":
            pend_del.append(a[i])
        else:
            pend_add.append(b[j])
    flush()
    return [f"{l[:col]:<{col}} {m} {r[:col]}" for l, m, r in rows]


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv and argv[0] in ("-h", "--help") else 2
    ctx = 3
    if "-u" in argv:
        i = argv.index("-u")
        ctx = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    files = [x for x in argv if not x.startswith("-")]
    a = open(files[0], encoding="utf-8", errors="replace").read().splitlines()
    b = open(files[1], encoding="utf-8", errors="replace").read().splitlines()
    if "-w" in argv:
        ka, kb = [" ".join(s.split()) for s in a], [" ".join(s.split()) for s in b]
        ops = myers(ka, kb)
    else:
        ops = myers(a, b)
    if all(op[0] == "=" for op in ops):
        return 0
    color = "--no-color" not in argv and sys.stdout.isatty()
    lines = side_by_side(a, b, ops) if "--side" in argv else unified(a, b, ops, ctx, color, tuple(files))
    print("\n".join(lines))
    return 1


def _selftest() -> None:
    import random

    def apply(a, b, ops):
        return [b[j] if k == "+" else a[i] for k, i, j in ops if k != "-"]

    rng = random.Random(1)
    for _ in range(300):
        a = [rng.choice("abc") for _ in range(rng.randint(0, 12))]
        b = [rng.choice("abc") for _ in range(rng.randint(0, 12))]
        ops = myers(a, b)
        assert apply(a, b, ops) == b
        assert [a[i] for k, i, _ in ops if k != "+"] == a
        # optimality vs. an LCS dynamic programme
        L = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
        for i in range(len(a) - 1, -1, -1):
            for j in range(len(b) - 1, -1, -1):
                L[i][j] = L[i + 1][j + 1] + 1 if a[i] == b[j] else max(L[i + 1][j], L[i][j + 1])
        assert sum(k != "=" for k, _, _ in ops) == len(a) + len(b) - 2 * L[0][0]
    u = unified(["x", "y", "z"], ["x", "Y", "z"], myers(["x", "y", "z"], ["x", "Y", "z"]), color=False)
    assert u[2] == "@@ -1,3 +1,3 @@" and "-y" in u and "+Y" in u
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        _selftest()
    else:
        sys.exit(main(sys.argv[1:]))
