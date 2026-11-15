"""Gale-Shapley stable matching, verified by a blocking-pair check.

Usage: python stable_marriage.py [n] [seed]
"""
import random
import sys


def gale_shapley(men: list[list[int]], women: list[list[int]]) -> list[int]:
    """Return wife[m] for each man m (proposer-optimal stable matching)."""
    n = len(men)
    rank = [{m: r for r, m in enumerate(pref)} for pref in women]
    nxt = [0] * n
    husband = [-1] * n
    free = list(range(n))
    while free:
        m = free.pop()
        w = men[m][nxt[m]]
        nxt[m] += 1
        h = husband[w]
        if h == -1:
            husband[w] = m
        elif rank[w][m] < rank[w][h]:
            husband[w] = m
            free.append(h)
        else:
            free.append(m)
    wife = [0] * n
    for w, m in enumerate(husband):
        wife[m] = w
    return wife


def blocking_pairs(men, women, wife) -> list[tuple[int, int]]:
    n = len(men)
    husband = [0] * n
    for m, w in enumerate(wife):
        husband[w] = m
    mr = [{w: r for r, w in enumerate(p)} for p in men]
    wr = [{m: r for r, m in enumerate(p)} for p in women]
    return [(m, w) for m in range(n) for w in range(n)
            if mr[m][w] < mr[m][wife[m]] and wr[w][m] < wr[w][husband[w]]]


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    men = [rng.sample(range(n), n) for _ in range(n)]
    women = [rng.sample(range(n), n) for _ in range(n)]
    wife = gale_shapley(men, women)
    for m, w in enumerate(wife):
        print(f"man {m} <-> woman {w} (his choice #{men[m].index(w) + 1})")
    bp = blocking_pairs(men, women, wife)
    print("blocking pairs:", bp or "none (stable)")
    assert not bp


if __name__ == "__main__":
    main()
