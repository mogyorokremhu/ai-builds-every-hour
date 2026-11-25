"""1-D random walk: expected distance ~ sqrt(2n/pi) and return-to-origin chance."""
import math
import random


def mean_abs_position(steps: int, trials: int = 4000, seed: int = 11) -> float:
    rng = random.Random(seed)
    total = 0
    for _ in range(trials):
        total += abs(sum(rng.choice((-1, 1)) for _ in range(steps)))
    return total / trials


def returned_to_origin(steps: int, trials: int = 3000, seed: int = 13) -> float:
    rng = random.Random(seed)
    back = 0
    for _ in range(trials):
        pos = 0
        for _ in range(steps):
            pos += rng.choice((-1, 1))
            if pos == 0:
                back += 1
                break
    return back / trials


if __name__ == "__main__":
    n = 400
    theory = math.sqrt(2 * n / math.pi)
    got = mean_abs_position(n)
    print(f"E|S_{n}| theory={theory:.2f} simulated={got:.2f}")
    print(f"P(return within 200 steps) ~ {returned_to_origin(200):.3f}")
    assert abs(got - theory) < 1.0
    print("ok")
