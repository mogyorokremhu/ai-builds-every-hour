"""Score (range) voting: ranks are converted to 0-10 scores linearly; highest mean wins."""
from ballots import CANDIDATES, random_ballots


def score(ballots, top=10):
    """Return (winner, mean score per candidate)."""
    n = len(CANDIDATES) - 1
    totals = {c: 0.0 for c in CANDIDATES}
    for b in ballots:
        for i, c in enumerate(b):
            totals[c] += top * (n - i) / n
    means = {c: t / len(ballots) for c, t in totals.items()}
    return max(means, key=means.get), means


if __name__ == "__main__":
    w, m = score(random_ballots(25, seed=3))
    for c, v in sorted(m.items(), key=lambda kv: -kv[1]):
        print(f"{c:3} {v:5.2f}")
    print("winner:", w)
