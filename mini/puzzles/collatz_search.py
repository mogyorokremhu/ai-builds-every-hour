#!/usr/bin/env python3
"""Collatz explorer: longest chain below a limit, with a memo table.

usage: collatz_search.py [LIMIT]   (default 100000)
       collatz_search.py --path N  print the chain for N
"""
import sys


def longest(limit):
    memo = {1: 1}
    best = (1, 1)
    for start in range(2, limit):
        n, stack = start, []
        while n not in memo:
            stack.append(n)
            n = n // 2 if n % 2 == 0 else 3 * n + 1
        length = memo[n]
        for v in reversed(stack):
            length += 1
            memo[v] = length
        if memo[start] > best[1]:
            best = (start, memo[start])
    return best


def path(n):
    out = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        out.append(n)
    return out


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--path":
        p = path(int(sys.argv[2]))
        print(len(p), "terms:", " ".join(map(str, p)))
    else:
        lim = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
        s, l = longest(lim)
        print(f"below {lim}: start {s}, chain length {l}")
