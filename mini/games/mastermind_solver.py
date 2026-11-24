"""Mastermind (6 colours, 4 pegs): Knuth-style minimax solver vs a random secret. Prints guesses."""
import itertools
import random
from collections import Counter

COLORS = "ABCDEF"


def score(secret: str, guess: str) -> tuple[int, int]:
    """Return (black, white) pegs."""
    black = sum(s == g for s, g in zip(secret, guess))
    common = sum((Counter(secret) & Counter(guess)).values())
    return black, common - black


def solve(secret: str) -> list[str]:
    pool = ["".join(p) for p in itertools.product(COLORS, repeat=4)]
    guess, guesses = "AABB", []
    while True:
        guesses.append(guess)
        fb = score(secret, guess)
        if fb == (4, 0):
            return guesses
        pool = [c for c in pool if score(c, guess) == fb]
        # minimax over remaining candidates (keeps it fast enough)
        guess = min(pool, key=lambda c: max(Counter(score(x, c) for x in pool).values()))


if __name__ == "__main__":
    secret = "".join(random.choice(COLORS) for _ in range(4))
    gs = solve(secret)
    print("secret:", secret)
    for i, g in enumerate(gs, 1):
        print(i, g, score(secret, g))
    print(f"solved in {len(gs)} guesses")
