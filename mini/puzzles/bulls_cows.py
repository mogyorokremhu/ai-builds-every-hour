#!/usr/bin/env python3
"""bulls_cows - Bulls and Cows (Mastermind with unique digits): solver + self-play.

  python3 bulls_cows.py --solve 4271     solver guesses the secret, prints each guess
  python3 bulls_cows.py --stats 200      average guesses over N random secrets
"""
import random
import sys
from itertools import permutations


def score(secret, guess):
    bulls = sum(a == b for a, b in zip(secret, guess))
    cows = len(set(secret) & set(guess)) - bulls
    return bulls, cows


def solve(secret, n=4):
    pool = ["".join(p) for p in permutations("0123456789", n)]
    total = len(pool)
    guesses = []
    while True:
        g = pool[0] if len(pool) == total else pool[len(pool) // 2]
        guesses.append(g)
        fb = score(secret, g)
        if fb == (n, 0):
            return guesses
        pool = [c for c in pool if score(c, g) == fb]


def main(argv):
    if len(argv) >= 2 and argv[0] == "--solve":
        for i, g in enumerate(solve(argv[1]), 1):
            print(i, g, score(argv[1], g))
    elif len(argv) >= 2 and argv[0] == "--stats":
        rng = random.Random(1)
        tot = 0
        n = int(argv[1])
        for _ in range(n):
            tot += len(solve("".join(rng.sample("0123456789", 4))))
        print(f"average guesses over {n}: {tot / n:.2f}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
