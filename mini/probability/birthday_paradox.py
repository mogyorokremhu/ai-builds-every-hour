"""Birthday paradox: exact probability vs. Monte Carlo simulation."""
import random


def exact(n: int, days: int = 365) -> float:
    """Probability that at least two of n people share a birthday."""
    p_unique = 1.0
    for i in range(n):
        p_unique *= (days - i) / days
    return 1 - p_unique


def simulate(n: int, trials: int = 20000, days: int = 365, seed: int = 1) -> float:
    rng = random.Random(seed)
    hits = sum(len({rng.randrange(days) for _ in range(n)}) < n for _ in range(trials))
    return hits / trials


if __name__ == "__main__":
    for n in (10, 23, 40, 57):
        print(f"n={n:2d} exact={exact(n):.4f} simulated={simulate(n):.4f}")
    assert abs(exact(23) - 0.5073) < 1e-3
    assert abs(simulate(23) - exact(23)) < 0.02
    print("ok")
