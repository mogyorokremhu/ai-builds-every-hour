"""Dice-pool success counting (World-of-Darkness style): roll N d10, count hits >= target."""
import random
import sys
from math import comb


def pool_successes(pool: int, target: int, rng: random.Random, sides: int = 10) -> int:
    """Roll `pool` dice; each die >= target is a success."""
    return sum(1 for _ in range(pool) if rng.randint(1, sides) >= target)


def exact_distribution(pool: int, target: int, sides: int = 10) -> list[float]:
    """P(k successes) for k = 0..pool (binomial)."""
    p = (sides - target + 1) / sides
    return [comb(pool, k) * p**k * (1 - p) ** (pool - k) for k in range(pool + 1)]


def main() -> None:
    pool = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    target = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    rng = random.Random(3)
    trials = 20000
    counts = [0] * (pool + 1)
    for _ in range(trials):
        counts[pool_successes(pool, target, rng)] += 1
    exact = exact_distribution(pool, target)
    print(f"pool={pool} target>={target}")
    for k in range(pool + 1):
        print(f"{k:2d} sim={counts[k] / trials:.4f} exact={exact[k]:.4f} " + "#" * round(exact[k] * 60))


if __name__ == "__main__":
    main()
