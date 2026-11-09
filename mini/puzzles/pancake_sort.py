"""Pancake sorting: greedy flips plus an optimal BFS flip count for small stacks.

Usage: python pancake_sort.py [n ...stack]   e.g. python pancake_sort.py 3 1 4 2
"""
import sys
from collections import deque
from itertools import permutations


def flip(s, k):
    return s[:k][::-1] + s[k:]


def greedy(stack):
    """Sort with at most 2n-3 flips; returns the list of flip sizes."""
    s, out = tuple(stack), []
    for size in range(len(s), 1, -1):
        m = s.index(max(s[:size]))
        if m == size - 1:
            continue
        if m:
            s = flip(s, m + 1)
            out.append(m + 1)
        s = flip(s, size)
        out.append(size)
    return out


def optimal(stack):
    """Fewest flips via BFS (fine up to ~8 pancakes)."""
    start, goal = tuple(stack), tuple(sorted(stack))
    seen, q = {start: 0}, deque([start])
    while q:
        s = q.popleft()
        if s == goal:
            return seen[s]
        for k in range(2, len(s) + 1):
            t = flip(s, k)
            if t not in seen:
                seen[t] = seen[s] + 1
                q.append(t)


def pancake_number(n):
    """Max over all stacks of n of the optimal flip count (A058986)."""
    return max(optimal(p) for p in permutations(range(n)))


if __name__ == "__main__":
    st = [int(a) for a in sys.argv[1:]] or [3, 6, 1, 5, 2, 4]
    print("stack  ", st)
    print("greedy ", greedy(st))
    print("optimal", optimal(st), "flips")
    print("pancake numbers n=1..6:", [pancake_number(n) for n in range(1, 7)])
