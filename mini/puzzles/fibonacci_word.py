#!/usr/bin/env python3
"""fibonacci_word - the Fibonacci word (a->ab, b->a) and its Zeckendorf link.

  python3 fibonacci_word.py 8        first 8 substitution steps' word length + prefix
  python3 fibonacci_word.py --zeck 100   Zeckendorf representation of 100
"""
import sys


def word(n):
    a, b = "a", "ab"
    if n == 0:
        return a
    for _ in range(n - 1):
        a, b = b, b + a
    return b


def zeckendorf(n):
    fibs = [1, 2]
    while fibs[-1] <= n:
        fibs.append(fibs[-1] + fibs[-2])
    out = []
    for f in reversed(fibs):
        if f <= n:
            out.append(f)
            n -= f
    return out


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--zeck":
        n = int(sys.argv[2])
        print(n, "=", " + ".join(map(str, zeckendorf(n))))
    else:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
        w = word(n)
        print(f"step {n}: length {len(w)}")
        print(w[:80])
