"""Instant-runoff (ranked-choice) voting vs plain plurality on the same ballots."""
from collections import Counter

from ballots import random_ballots


def plurality(ballots):
    """Winner = most first-place votes."""
    return Counter(b[0] for b in ballots).most_common(1)[0][0]


def irv(ballots, verbose=True):
    """Repeatedly eliminate the candidate with fewest first-choice votes."""
    remaining = set(ballots[0])
    rnd = 1
    while True:
        tally = Counter({c: 0 for c in remaining})
        for b in ballots:
            tally[next(c for c in b if c in remaining)] += 1
        if verbose:
            print(f"round {rnd}: " + ", ".join(f"{c}={v}" for c, v in sorted(tally.items())))
        top, votes = tally.most_common(1)[0]
        if votes * 2 > len(ballots) or len(remaining) == 1:
            return top
        loser = min(sorted(remaining), key=lambda c: tally[c])
        if verbose:
            print(f"  eliminate {loser}")
        remaining.remove(loser)
        rnd += 1


if __name__ == "__main__":
    bs = random_ballots(31, seed=4)
    print("plurality winner:", plurality(bs))
    print("IRV winner:", irv(bs))
