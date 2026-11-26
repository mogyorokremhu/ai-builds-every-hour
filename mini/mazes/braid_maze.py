"""Braid maze: a perfect maze with dead ends removed so it has loops: python braid_maze.py [w h seed]."""
import random
import sys

from wilson_maze import render, wilson


def braid(w: int, h: int, passages: set, rng: random.Random) -> set:
    """Knock down one wall at every dead end."""
    def neighbors(c):
        x, y = c
        return [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= x + dx < w and 0 <= y + dy < h]
    cells = [(x, y) for y in range(h) for x in range(w)]
    rng.shuffle(cells)
    for c in cells:
        open_n = [n for n in neighbors(c) if frozenset((c, n)) in passages]
        if len(open_n) == 1:
            closed = [n for n in neighbors(c) if frozenset((c, n)) not in passages]
            if closed:
                passages.add(frozenset((c, rng.choice(closed))))
    return passages


if __name__ == "__main__":
    a = sys.argv[1:]
    w, h = (int(a[0]), int(a[1])) if len(a) >= 2 else (12, 6)
    rng = random.Random(int(a[2])) if len(a) >= 3 else random.Random()
    print(render(w, h, braid(w, h, wilson(w, h, rng), rng)))
