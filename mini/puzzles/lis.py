"""Longest increasing subsequence in O(n log n) with patience sorting.

Usage: python lis.py [n1 n2 ...]   (random list if none)
"""
import random
import sys
from bisect import bisect_left


def lis(seq: list[int]) -> list[int]:
    tails: list[int] = []   # tails[k] = smallest tail of an increasing run of length k+1
    idx: list[int] = []     # index in seq of each tail
    prev = [-1] * len(seq)
    for i, x in enumerate(seq):
        k = bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
            idx.append(i)
        else:
            tails[k] = x
            idx[k] = i
        prev[i] = idx[k - 1] if k else -1
    out, i = [], idx[-1] if idx else -1
    while i >= 0:
        out.append(seq[i])
        i = prev[i]
    return out[::-1]


if __name__ == "__main__":
    seq = [int(a) for a in sys.argv[1:]] or random.sample(range(100), 20)
    print("sequence:", seq)
    r = lis(seq)
    print("LIS length", len(r), ":", r)
