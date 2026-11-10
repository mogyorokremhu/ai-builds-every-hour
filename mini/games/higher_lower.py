"""Higher/Lower: guess a number 1-100 in 7 tries. `--auto` binary-searches for you."""
import random
import sys


def main() -> None:
    secret = random.randint(1, 100)
    lo, hi = 1, 100
    for turn in range(1, 8):
        if "--auto" in sys.argv:
            guess = (lo + hi) // 2
            print(f"guess {turn}: {guess}")
        else:
            try:
                guess = int(input(f"guess {turn}/7> "))
            except (EOFError, ValueError):
                return
        if guess == secret:
            print(f"Correct in {turn}!")
            return
        if guess < secret:
            lo = max(lo, guess + 1)
            print("higher")
        else:
            hi = min(hi, guess - 1)
            print("lower")
    print(f"Out of tries. It was {secret}.")


if __name__ == "__main__":
    main()
