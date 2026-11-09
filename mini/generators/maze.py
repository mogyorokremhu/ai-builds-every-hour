"""Maze generator: recursive backtracker, printed as ASCII. Usage: python maze.py [W H] [seed]"""
import random
import sys


def generate(w: int, h: int, rng: random.Random):
    seen = {(0, 0)}
    open_walls = set()
    stack = [(0, 0)]
    while stack:
        x, y = stack[-1]
        nbrs = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= x + dx < w and 0 <= y + dy < h and (x + dx, y + dy) not in seen]
        if not nbrs:
            stack.pop()
            continue
        n = rng.choice(nbrs)
        seen.add(n)
        open_walls.add(frozenset(((x, y), n)))
        stack.append(n)
    return open_walls


def render(w: int, h: int, open_walls) -> str:
    rows = ["+" + "--+" * w]
    for y in range(h):
        line, under = "|", "+"
        for x in range(w):
            line += "  " + (" " if frozenset(((x, y), (x + 1, y))) in open_walls else "|")
            under += ("  " if frozenset(((x, y), (x, y + 1))) in open_walls else "--") + "+"
        rows += [line, under]
    return "\n".join(rows)


if __name__ == "__main__":
    a = sys.argv[1:]
    w, h = (int(a[0]), int(a[1])) if len(a) >= 2 else (12, 6)
    rng = random.Random(int(a[2])) if len(a) > 2 else random.Random()
    print(render(w, h, generate(w, h, rng)))
