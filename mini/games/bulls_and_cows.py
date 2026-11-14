"""Bulls and Cows: guess a 4-digit code with distinct digits. `--auto` solves by elimination."""
import itertools
import random
import sys


def score(secret: str, guess: str) -> tuple[int, int]:
    bulls = sum(a == b for a, b in zip(secret, guess))
    return bulls, len(set(secret) & set(guess)) - bulls


def main() -> None:
    pool = ["".join(p) for p in itertools.permutations("0123456789", 4)]
    secret = random.choice(pool)
    for turn in range(1, 11):
        if "--auto" in sys.argv:
            guess = pool[len(pool) // 2] if len(pool) > 1 else pool[0]
        else:
            try:
                guess = input(f"guess {turn}/10> ").strip()
            except EOFError:
                return
            if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
                continue
        b, c = score(secret, guess)
        print(f"{guess}: {b} bulls, {c} cows")
        if b == 4:
            print(f"cracked in {turn}!")
            return
        pool = [p for p in pool if score(p, guess) == (b, c)]
    print(f"out of turns; it was {secret}")


if __name__ == "__main__":
    main()
