"""Plurality (first-past-the-post) with a runoff check: winner needs >50% or the top two go to a runoff."""
from collections import Counter

from ballots import random_ballots


def plurality(ballots):
    """Return (winner, first-choice tally)."""
    tally = Counter(b[0] for b in ballots)
    return tally.most_common(1)[0][0], tally


def runoff(ballots, a, b):
    """Head-to-head between a and b using each ballot's ranking."""
    wa = sum(1 for x in ballots if x.index(a) < x.index(b))
    return (a, wa, len(ballots) - wa) if wa * 2 > len(ballots) else (b, len(ballots) - wa, wa)


if __name__ == "__main__":
    ballots = random_ballots(31, seed=4)
    w, tally = plurality(ballots)
    print("first choices:", dict(tally))
    if tally[w] * 2 > len(ballots):
        print("majority winner:", w)
    else:
        (a, _), (b, _) = tally.most_common(2)
        win, v1, v2 = runoff(ballots, a, b)
        print(f"no majority; runoff {a} vs {b}: {win} wins {v1}-{v2}")
