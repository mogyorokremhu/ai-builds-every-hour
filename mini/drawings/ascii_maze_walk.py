"""Recursive-backtracker maze drawn with box characters.  python ascii_maze_walk.py [w h seed]"""
import random, sys

def main(w=20, h=8, seed=1):
    random.seed(seed)
    seen = {(0, 0)}
    open_ = set()
    stack = [(0, 0)]
    while stack:
        x, y = stack[-1]
        nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
              if 0 <= x + dx < w and 0 <= y + dy < h and (x + dx, y + dy) not in seen]
        if not nb:
            stack.pop()
            continue
        n = random.choice(nb)
        seen.add(n)
        open_.add(frozenset(((x, y), n)))
        stack.append(n)
    print("+" + "--+" * w)
    for y in range(h):
        row, under = "|", "+"
        for x in range(w):
            row += "  " + (" " if frozenset(((x, y), (x + 1, y))) in open_ else "|")
            under += ("  " if frozenset(((x, y), (x, y + 1))) in open_ else "--") + "+"
        print(row)
        print(under)

if __name__ == "__main__":
    a = [int(v) for v in sys.argv[1:4]]
    main(*a)
