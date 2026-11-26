"""Shared helpers: random ranked ballots for a few candidates (used by the other voting demos)."""
import random

CANDIDATES = ["Ada", "Bo", "Cy", "Di"]


def random_ballots(n: int = 25, seed: int = 1, candidates=CANDIDATES) -> list[list[str]]:
    """Return n ballots, each a full ranking (best first)."""
    rng = random.Random(seed)
    # biased weights so there is some structure
    weights = {c: rng.random() + 0.3 for c in candidates}
    ballots = []
    for _ in range(n):
        pool = list(candidates)
        ranking = []
        while pool:
            pick = rng.choices(pool, weights=[weights[c] for c in pool])[0]
            ranking.append(pick)
            pool.remove(pick)
        ballots.append(ranking)
    return ballots


if __name__ == "__main__":
    for b in random_ballots(5):
        print(" > ".join(b))
