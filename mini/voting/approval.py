"""Approval voting derived from ranked ballots: each voter approves their top k candidates."""
from collections import Counter

from ballots import random_ballots


def approval(ballots, k=2):
    """Return (winner, approvals) where each ballot approves its top k."""
    tally = Counter()
    for b in ballots:
        tally.update(b[:k])
    return tally.most_common(1)[0][0], tally


if __name__ == "__main__":
    ballots = random_ballots(25, seed=2)
    for k in (1, 2, 3):
        w, t = approval(ballots, k)
        print(f"approve top {k}: winner {w}  {dict(t)}")
