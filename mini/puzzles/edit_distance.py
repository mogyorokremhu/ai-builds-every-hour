#!/usr/bin/env python3
"""edit_distance - Levenshtein distance with an edit script (DP + backtrack)."""
import sys


def edit_script(a: str, b: str) -> tuple[int, list[str]]:
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    ops, i, j = [], n, m
    while i or j:
        if i and j and d[i][j] == d[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            if a[i - 1] != b[j - 1]:
                ops.append(f"sub {a[i-1]}->{b[j-1]}")
            i, j = i - 1, j - 1
        elif i and d[i][j] == d[i - 1][j] + 1:
            ops.append(f"del {a[i-1]}"); i -= 1
        else:
            ops.append(f"ins {b[j-1]}"); j -= 1
    return d[n][m], ops[::-1]


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert edit_script("kitten", "sitting")[0] == 3
        assert edit_script("", "abc")[0] == 3
        assert edit_script("abc", "abc") == (0, [])
        assert edit_script("flaw", "lawn")[0] == 2
        print("ok"); sys.exit()
    a, b = (sys.argv[1:3] + ["kitten", "sitting"])[:2]
    dist, ops = edit_script(a, b)
    print(f"{a} -> {b}: distance {dist}")
    for o in ops:
        print(" ", o)
