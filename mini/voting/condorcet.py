"""Condorcet / Copeland / Borda on the same ballots: pairwise matrix and winners."""
from itertools import combinations

from ballots import CANDIDATES, random_ballots


def pairwise(ballots):
    """wins[a][b] = number of ballots ranking a above b."""
    wins = {a: {b: 0 for b in CANDIDATES} for a in CANDIDATES}
    for b in ballots:
        pos = {c: i for i, c in enumerate(b)}
        for x, y in combinations(CANDIDATES, 2):
            if pos[x] < pos[y]:
                wins[x][y] += 1
            else:
                wins[y][x] += 1
    return wins


def condorcet_winner(wins, n):
    for a in CANDIDATES:
        if all(wins[a][b] * 2 > n for b in CANDIDATES if b != a):
            return a
    return None


def copeland(wins):
    score = {a: sum((wins[a][b] > wins[b][a]) - (wins[a][b] < wins[b][a])
                    for b in CANDIDATES if b != a) for a in CANDIDATES}
    return max(score, key=score.get), score


def borda(ballots):
    pts = {c: 0 for c in CANDIDATES}
    for b in ballots:
        for i, c in enumerate(b):
            pts[c] += len(b) - 1 - i
    return max(pts, key=pts.get), pts


if __name__ == "__main__":
    bs = random_ballots(31, seed=4)
    w = pairwise(bs)
    print("      " + " ".join(f"{c:>3}" for c in CANDIDATES))
    for a in CANDIDATES:
        print(f"{a:>5} " + " ".join(f"{w[a][b]:>3}" if a != b else "  -" for b in CANDIDATES))
    print("Condorcet winner:", condorcet_winner(w, len(bs)))
    print("Copeland:", copeland(w))
    print("Borda:", borda(bs))
