#!/usr/bin/env python3
"""permutation_rank - rank/unrank permutations in lexicographic order (factorial number system).

  python3 permutation_rank.py rank 3 1 2 0
  python3 permutation_rank.py unrank 4 17
"""
import sys
from math import factorial


def rank(perm):
    items = sorted(perm)
    r = 0
    for i, p in enumerate(perm):
        idx = items.index(p)
        r += idx * factorial(len(perm) - 1 - i)
        items.pop(idx)
    return r


def unrank(n, r):
    items = list(range(n))
    out = []
    for i in range(n, 0, -1):
        idx, r = divmod(r, factorial(i - 1))
        out.append(items.pop(idx))
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "rank":
        print(rank(list(map(int, sys.argv[2:]))))
    elif cmd == "unrank":
        print(*unrank(int(sys.argv[2]), int(sys.argv[3])))
    else:
        print(__doc__)
