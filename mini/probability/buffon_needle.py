"""Buffon's needle: estimate pi by dropping needles on a lined floor."""
import math
import random


def estimate_pi(drops: int = 200000, needle: float = 1.0, gap: float = 2.0, seed: int = 7) -> float:
    rng = random.Random(seed)
    hits = 0
    for _ in range(drops):
        y = rng.uniform(0, gap / 2)          # centre distance to nearest line
        angle = rng.uniform(0, math.pi / 2)  # needle angle
        if y <= (needle / 2) * math.sin(angle):
            hits += 1
    return (2 * needle * drops) / (gap * hits)


if __name__ == "__main__":
    est = estimate_pi()
    print(f"pi ~ {est:.4f}")
    assert abs(est - math.pi) < 0.05
    print("ok")
