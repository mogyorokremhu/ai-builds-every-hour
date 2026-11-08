"""Mastermind: a codebreaker that always wins classic Mastermind in at most 5 guesses.

Classic rules: a secret of 4 pegs from 6 colours (repeats allowed). Each guess is scored
with black pegs (right colour, right place) and white pegs (right colour, wrong place).
The solver uses Knuth's minimax strategy: pick the guess whose worst-case feedback leaves
the fewest candidate codes.

Run: python mastermind.py [SECRET]      e.g.  python mastermind.py 3416
     python mastermind.py --play        you guess a random code instead
"""
from __future__ import annotations

import itertools
import random
import sys
from collections import Counter

COLORS = "123456"
PEGS = 4
ALL_CODES = ["".join(p) for p in itertools.product(COLORS, repeat=PEGS)]


def score(guess: str, secret: str) -> tuple[int, int]:
    """(black, white) feedback for ``guess`` against ``secret``."""
    black = sum(g == s for g, s in zip(guess, secret))
    common = sum((Counter(guess) & Counter(secret)).values())
    return black, common - black


def best_guess(candidates: list[str]) -> str:
    """Knuth minimax: minimise the largest feedback partition (prefer candidates on ties)."""
    if len(candidates) == 1:
        return candidates[0]
    cand_set = set(candidates)
    best, best_key = None, None
    for g in ALL_CODES:
        parts = Counter(score(g, c) for c in candidates)
        key = (max(parts.values()), g not in cand_set, g)
        if best_key is None or key < best_key:
            best, best_key = g, key
    return best


def solve(secret: str, verbose: bool = True) -> list[str]:
    candidates = list(ALL_CODES)
    guesses: list[str] = []
    guess = "1122"  # Knuth's optimal opening
    while True:
        guesses.append(guess)
        fb = score(guess, secret)
        if verbose:
            print(f"guess {len(guesses)}: {guess}  ->  {'●' * fb[0]}{'○' * fb[1]}{'·' * (PEGS - sum(fb))}"
                  f"   ({len(candidates)} codes were possible)")
        if fb == (PEGS, 0):
            return guesses
        candidates = [c for c in candidates if score(guess, c) == fb]
        guess = best_guess(candidates)


def play() -> None:
    secret = random.choice(ALL_CODES)
    print(f"I picked a code of {PEGS} digits from {COLORS}. ● = right place, ○ = wrong place.")
    for turn in range(1, 11):
        g = input(f"guess {turn}> ").strip()
        if len(g) != PEGS or any(ch not in COLORS for ch in g):
            print(f"enter {PEGS} digits from {COLORS}")
            continue
        b, w = score(g, secret)
        print("●" * b + "○" * w or "nothing")
        if b == PEGS:
            print(f"Cracked in {turn}!")
            return
    print(f"Out of guesses — it was {secret}.")


def main() -> None:
    if "--play" in sys.argv:
        play()
        return
    secret = sys.argv[1] if len(sys.argv) > 1 else random.choice(ALL_CODES)
    if len(secret) != PEGS or any(ch not in COLORS for ch in secret):
        raise SystemExit(f"secret must be {PEGS} digits from {COLORS}")
    print(f"Secret: {secret}\n")
    guesses = solve(secret)
    print(f"\nSolved in {len(guesses)} guesses.")


if __name__ == "__main__":
    main()
