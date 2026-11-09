"""Kaprekar's routine: sort digits desc - asc until reaching a fixed point or cycle.

Usage: python kaprekar.py [number] [digits]
"""
import sys


def step(n, digits):
    d = f"{n:0{digits}d}"
    return int("".join(sorted(d, reverse=True))) - int("".join(sorted(d)))


def chain(n, digits=4):
    """Return the orbit until a value repeats."""
    seen, out = set(), []
    while n not in seen:
        seen.add(n)
        out.append(n)
        n = step(n, digits)
    return out + [n]


def max_steps(digits=4):
    """Worst-case steps to reach the constant over all digit strings (4 digits -> 7)."""
    worst = 0
    for n in range(10 ** digits):
        if len(set(f"{n:0{digits}d}")) == 1:
            continue
        c = chain(n, digits)
        worst = max(worst, len(c) - 2)
    return worst


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3524
    d = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    print(" -> ".join(map(str, chain(n, d))))
    print(f"worst case for {d} digits: {max_steps(d)} steps")
