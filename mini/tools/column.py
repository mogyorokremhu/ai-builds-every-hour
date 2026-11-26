#!/usr/bin/env python3
"""column - align delimited text from stdin or files into padded columns.

Usage: column.py [-d DELIM] [-s GAP] [-r] [file ...]   (-r right-aligns numbers)
"""
import sys


def align(lines: list[str], delim: str | None = None, gap: int = 2, right_numbers: bool = False) -> list[str]:
    rows = [ln.split(delim) if delim else ln.split() for ln in lines if ln.strip()]
    if not rows:
        return []
    ncol = max(map(len, rows))
    widths = [max((len(r[i]) for r in rows if i < len(r)), default=0) for i in range(ncol)]

    def isnum(s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False

    out = []
    for r in rows:
        cells = []
        for i, c in enumerate(r):
            last = i == len(r) - 1
            if right_numbers and isnum(c):
                cells.append(c.rjust(widths[i]))
            else:
                cells.append(c if last else c.ljust(widths[i]))
        out.append((" " * gap).join(cells).rstrip())
    return out


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert align(["a bb", "ccc d"]) == ["a    bb", "ccc  d"]
        assert align(["x,1", "yy,22"], ",", 1, True) == ["x   1", "yy 22"]
        assert align([]) == []
        print("ok")
        sys.exit()
    args = sys.argv[1:]
    delim, gap, right = None, 2, False
    files = []
    while args:
        a = args.pop(0)
        if a == "-d":
            delim = args.pop(0)
        elif a == "-s":
            gap = int(args.pop(0))
        elif a == "-r":
            right = True
        else:
            files.append(a)
    text = "".join(open(f).read() for f in files) if files else sys.stdin.read()
    print("\n".join(align(text.splitlines(), delim, gap, right)))
