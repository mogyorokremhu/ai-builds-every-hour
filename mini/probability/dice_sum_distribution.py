"""Distribution of the sum of n dice: exact convolution vs. simulation."""
import random
from collections import Counter


def exact(n: int, sides: int = 6) -> dict[int, float]:
    dist = {0: 1.0}
    for _ in range(n):
        new: dict[int, float] = {}
        for s, p in dist.items():
            for f in range(1, sides + 1):
                new[s + f] = new.get(s + f, 0.0) + p / sides
        dist = new
    return dist


def simulate(n: int, sides: int = 6, trials: int = 60000, seed: int = 5) -> dict[int, float]:
    rng = random.Random(seed)
    c = Counter(sum(rng.randint(1, sides) for _ in range(n)) for _ in range(trials))
    return {k: v / trials for k, v in c.items()}


if __name__ == "__main__":
    e, s = exact(3), simulate(3)
    for k in sorted(e):
        print(f"{k:2d} {e[k]:.4f} {s.get(k, 0):.4f} " + "#" * round(e[k] * 200))
    assert abs(sum(e.values()) - 1) < 1e-9
    assert max(abs(e[k] - s.get(k, 0)) for k in e) < 0.01
    print("ok")
