#!/usr/bin/env python3
"""Convert CSV (stdin or file) to an aligned Markdown table.

Usage: csv2md.py [FILE] [-d SEP] [--selftest]
Numeric columns are right-aligned.
"""
from __future__ import annotations
import csv
import io
import sys


def to_markdown(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    n = max(len(r) for r in rows)
    rows = [r + [""] * (n - len(r)) for r in rows]
    esc = [[c.replace("|", "\\|") for c in r] for r in rows]
    widths = [max(3, *(len(r[i]) for r in esc)) for i in range(n)]

    def isnum(s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False

    right = [all(isnum(r[i]) for r in esc[1:] if r[i]) and len(esc) > 1 for i in range(n)]
    fmt = lambda r: "| " + " | ".join(
        c.rjust(w) if right[i] else c.ljust(w) for i, (c, w) in enumerate(zip(r, widths))) + " |"
    sep = "| " + " | ".join(("-" * (w - 1) + ":") if right[i] else "-" * w
                            for i, w in enumerate(widths)) + " |"
    return "\n".join([fmt(esc[0]), sep] + [fmt(r) for r in esc[1:]])


def selftest() -> None:
    rows = list(csv.reader(io.StringIO("name,qty\napple,3\nfig,12\n")))
    out = to_markdown(rows).splitlines()
    assert out[0].startswith("| name ") and out[2].endswith("  3 |"), out
    assert out[1].endswith("--: |"), out[1]
    print("ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit()
    args = sys.argv[1:]
    sep = args[args.index("-d") + 1] if "-d" in args else ","
    files = [a for i, a in enumerate(args) if not a.startswith("-") and (i == 0 or args[i - 1] != "-d")]
    src = open(files[0], newline="") if files else sys.stdin
    print(to_markdown(list(csv.reader(src, delimiter=sep))))
