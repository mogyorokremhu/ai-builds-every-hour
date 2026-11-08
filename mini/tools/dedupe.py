#!/usr/bin/env python3
"""dedupe - drop repeated lines from stdin/files, keeping first occurrences (-c counts, -i ignore case)."""
import sys
from collections import Counter

def dedupe(lines, ignore_case=False):
    seen, counts, order = set(), Counter(), []
    for l in lines:
        k = l.lower() if ignore_case else l
        counts[k] += 1
        if k not in seen: seen.add(k); order.append((k, l))
    return [(l, counts[k]) for k, l in order]

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert dedupe(["a", "b", "A", "a"], True) == [("a", 3), ("b", 1)]; print("ok"); sys.exit()
    ic, show = "-i" in sys.argv, "-c" in sys.argv
    files = [a for a in sys.argv[1:] if not a.startswith("-")]
    src = [l.rstrip("\n") for f in files for l in open(f)] if files else [l.rstrip("\n") for l in sys.stdin]
    for l, c in dedupe(src, ic): print(f"{c:>5} {l}" if show else l)
