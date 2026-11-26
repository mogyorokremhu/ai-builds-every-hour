#!/usr/bin/env python3
"""interval - merge overlapping numeric ranges, e.g. `interval.py 1-5 3-8 10-12` -> 1-8 10-12.

With --gaps, prints the gaps between merged ranges instead. Ranges may also come from stdin.
"""
import sys


def parse(tok: str) -> tuple[int, int]:
    a, _, b = tok.partition("-")
    lo, hi = int(a), int(b or a)
    return (lo, hi) if lo <= hi else (hi, lo)


def merge(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for lo, hi in sorted(ranges):
        if out and lo <= out[-1][1] + 1:
            out[-1] = (out[-1][0], max(out[-1][1], hi))
        else:
            out.append((lo, hi))
    return out


def gaps(merged: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [(a[1] + 1, b[0] - 1) for a, b in zip(merged, merged[1:])]


def fmt(r: tuple[int, int]) -> str:
    return str(r[0]) if r[0] == r[1] else f"{r[0]}-{r[1]}"


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert merge([(1, 5), (3, 8), (10, 12)]) == [(1, 8), (10, 12)]
        assert merge([(1, 2), (3, 4)]) == [(1, 4)]
        assert gaps([(1, 8), (10, 12), (20, 20)]) == [(9, 9), (13, 19)]
        assert parse("7") == (7, 7) and parse("9-2") == (2, 9)
        print("ok")
        sys.exit()
    toks = [a for a in sys.argv[1:] if a != "--gaps"] or sys.stdin.read().split()
    m = merge([parse(t) for t in toks])
    print(" ".join(fmt(r) for r in (gaps(m) if "--gaps" in sys.argv else m)))
