"""Coupon collector: expected draws to collect all n coupons, exact vs. simulated."""
import random


def exact(n: int) -> float:
    """Expected draws = n * H(n)."""
    return n * sum(1 / k for k in range(1, n + 1))


def simulate(n: int, trials: int = 5000, seed: int = 5) -> float:
    rng = random.Random(seed)
    total = 0
    for _ in range(trials):
        seen, draws = set(), 0
        while len(seen) < n:
            seen.add(rng.randrange(n))
            draws += 1
        total += draws
    return total / trials


if __name__ == "__main__":
    for n in (5, 10, 25):
        print(f"n={n:2d} exact={exact(n):.2f} simulated={simulate(n):.2f}")
    assert abs(exact(6) - 14.7) < 1e-9
    assert abs(simulate(10) - exact(10)) < 0.5
    print("ok")
