"""Simulate the casino game craps and estimate the pass-line win rate."""
import random
import sys


def roll(rng: random.Random) -> int:
    return rng.randint(1, 6) + rng.randint(1, 6)


def pass_line(rng: random.Random) -> bool:
    """Play one pass-line bet; True if the shooter wins."""
    first = roll(rng)
    if first in (7, 11):
        return True
    if first in (2, 3, 12):
        return False
    while True:
        r = roll(rng)
        if r == first:
            return True
        if r == 7:
            return False


def main() -> None:
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    rng = random.Random(42)
    wins = sum(pass_line(rng) for _ in range(trials))
    print(f"{trials} games, wins={wins}, rate={wins / trials:.4f} (exact 244/495={244 / 495:.4f})")


if __name__ == "__main__":
    main()
