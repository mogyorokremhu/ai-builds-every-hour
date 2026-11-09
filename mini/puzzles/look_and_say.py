"""Look-and-say sequence: 1, 11, 21, 1211, ... plus Conway's constant estimate."""
import sys
from itertools import groupby


def next_term(s: str) -> str:
    return "".join(f"{len(list(g))}{k}" for k, g in groupby(s))


def terms(n: int, start: str = "1"):
    s = start
    for _ in range(n):
        yield s
        s = next_term(s)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    lens = []
    for i, t in enumerate(terms(n), 1):
        lens.append(len(t))
        print(f"{i:2}: {t if len(t) < 60 else t[:57] + '...'}  (len {len(t)})")
    if len(lens) > 2:
        print(f"length ratio ~ {lens[-1] / lens[-2]:.4f} (Conway's constant ~ 1.3036)")
