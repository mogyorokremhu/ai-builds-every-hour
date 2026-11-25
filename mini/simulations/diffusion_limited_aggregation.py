"""Diffusion-limited aggregation: random walkers stick to a growing cluster. Usage: python diffusion_limited_aggregation.py [particles] [seed]"""
import random
import sys


def dla(particles: int = 150, size: int = 41, seed: int = 1):
    rng = random.Random(seed)
    c = size // 2
    stuck = {(c, c)}
    for _ in range(particles):
        while True:
            x, y = rng.choice([(1, rng.randrange(size)), (size - 2, rng.randrange(size)),
                               (rng.randrange(size), 1), (rng.randrange(size), size - 2)])
            if (x, y) not in stuck:
                break
        while True:
            if any((x + dx, y + dy) in stuck for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                stuck.add((x, y))
                break
            dx, dy = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
            x = min(max(x + dx, 1), size - 2)
            y = min(max(y + dy, 1), size - 2)
    return stuck, size


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    stuck, size = dla(n, seed=seed)
    for y in range(size):
        print("".join("#" if (x, y) in stuck else "." for x in range(size)))
    print(f"{len(stuck)} cells in cluster")
