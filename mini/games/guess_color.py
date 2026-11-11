"""Mastermind-lite: crack a 4-peg code of colors R G B Y O P. `--auto` uses elimination."""
import itertools
import random
import sys

COLORS = "RGBYOP"


def score(secret: str, guess: str) -> tuple[int, int]:
    exact = sum(a == b for a, b in zip(secret, guess))
    common = sum(min(secret.count(c), guess.count(c)) for c in COLORS)
    return exact, common - exact


def main() -> None:
    secret = "".join(random.choice(COLORS) for _ in range(4))
    pool = ["".join(p) for p in itertools.product(COLORS, repeat=4)]
    for turn in range(1, 11):
        if "--auto" in sys.argv:
            guess = pool[0]
        else:
            try:
                guess = input(f"guess {turn}/10 (e.g. RGBY)> ").strip().upper()
            except EOFError:
                return
            if len(guess) != 4 or set(guess) - set(COLORS):
                continue
        fb = score(secret, guess)
        print(f"{guess}: {fb[0]} exact, {fb[1]} misplaced")
        if fb[0] == 4:
            print(f"Cracked in {turn}!")
            return
        pool = [p for p in pool if score(p, guess) == fb]
    print("Out of guesses; code was", secret)


if __name__ == "__main__":
    main()
