"""Exploding dice: max roll rerolls and adds. Simulated mean vs. the exact mean."""
import random
import sys


def exploding_roll(sides: int, rng: random.Random) -> int:
    """Roll a die; on max, roll again and add (repeat)."""
    total = 0
    while True:
        r = rng.randint(1, sides)
        total += r
        if r != sides:
            return total


def exact_mean(sides: int) -> float:
    """Exact mean of an exploding die: ((s+1)/2) * s/(s-1)."""
    # E = (1/s)*sum_{i<s}(i) + (1/s)*(s + E)  =>  E(1 - 1/s) = (s-1)/2 + 1
    return (sides + 1) / 2 * sides / (sides - 1)


def main() -> None:
    sides = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    rng = random.Random(11)
    n = 50000
    rolls = [exploding_roll(sides, rng) for _ in range(n)]
    print(f"d{sides}! sim mean={sum(rolls) / n:.3f} exact={exact_mean(sides):.3f} max={max(rolls)}")


if __name__ == "__main__":
    main()
