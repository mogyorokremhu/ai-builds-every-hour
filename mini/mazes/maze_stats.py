"""Compare dead-end counts of Wilson vs braid mazes: python maze_stats.py."""
import random

from braid_maze import braid
from wilson_maze import wilson


def dead_ends(w, h, passages):
    deg = {}
    for p in passages:
        for c in p:
            deg[c] = deg.get(c, 0) + 1
    return sum(1 for v in deg.values() if v == 1)


if __name__ == "__main__":
    w, h = 15, 15
    for seed in range(3):
        p = wilson(w, h, random.Random(seed))
        print(f"seed {seed}: perfect passages={len(p)} (expect {w*h-1}) dead ends={dead_ends(w, h, p)}", end="")
        b = braid(w, h, set(p), random.Random(seed))
        print(f" | braid passages={len(b)} dead ends={dead_ends(w, h, b)}")
