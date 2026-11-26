"""Perfect maze via Wilson's algorithm (loop-erased random walks): python wilson_maze.py [w h seed]."""
import random
import sys


def wilson(w: int, h: int, rng: random.Random):
    """Return the set of carved passages as frozenset pairs of cells."""
    cells = [(x, y) for y in range(h) for x in range(w)]
    in_maze = {rng.choice(cells)}
    passages = set()
    for start in cells:
        if start in in_maze:
            continue
        nxt = {}
        cur = start
        while cur not in in_maze:
            x, y = cur
            opts = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                    if 0 <= x + dx < w and 0 <= y + dy < h]
            nxt[cur] = rng.choice(opts)
            cur = nxt[cur]
        cur = start
        while cur not in in_maze:
            in_maze.add(cur)
            passages.add(frozenset((cur, nxt[cur])))
            cur = nxt[cur]
    return passages


def render(w: int, h: int, passages) -> str:
    rows = ["+" + "---+" * w]
    for y in range(h):
        line, under = "|", "+"
        for x in range(w):
            line += "   "
            line += " " if frozenset(((x, y), (x + 1, y))) in passages else "|"
            under += "   +" if frozenset(((x, y), (x, y + 1))) in passages else "---+"
        rows += [line, under]
    return "\n".join(rows)


if __name__ == "__main__":
    a = sys.argv[1:]
    w, h = (int(a[0]), int(a[1])) if len(a) >= 2 else (12, 6)
    rng = random.Random(int(a[2])) if len(a) >= 3 else random.Random()
    print(render(w, h, wilson(w, h, rng)))
