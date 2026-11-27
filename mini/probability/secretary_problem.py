"""Secretary problem: skip the first n/e candidates, then take the next best-so-far."""
import math
import random


def trial(n: int, skip: int, rng: random.Random) -> bool:
    ranks = list(range(n))
    rng.shuffle(ranks)
    best_seen = max(ranks[:skip], default=-1)
    for r in ranks[skip:]:
        if r > best_seen:
            return r == n - 1
    return ranks[-1] == n - 1  # forced to take the last one


def success_rate(n: int = 50, skip: int | None = None, trials: int = 20000, seed: int = 3) -> float:
    rng = random.Random(seed)
    skip = round(n / math.e) if skip is None else skip
    return sum(trial(n, skip, rng) for _ in range(trials)) / trials


if __name__ == "__main__":
    best = success_rate()
    naive = success_rate(skip=0)
    print(f"skip n/e: {best:.3f}  (theory ~ {1/math.e:.3f})   take first: {naive:.3f}")
    assert abs(best - 0.37) < 0.03 and naive < 0.06
    print("ok")
