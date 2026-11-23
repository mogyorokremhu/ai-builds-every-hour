"""2D random walkers: mean squared displacement vs time. Usage: python random_walk_stats.py [walkers] [steps] [seed]"""
import random
import sys


def msd(walkers: int = 500, steps: int = 200, seed: int = 1) -> list[float]:
    """Mean squared displacement after each step (theory: equals the step count)."""
    rng = random.Random(seed)
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    xs = [0] * walkers
    ys = [0] * walkers
    out = []
    for _ in range(steps):
        for i in range(walkers):
            dx, dy = rng.choice(dirs)
            xs[i] += dx
            ys[i] += dy
        out.append(sum(x * x + y * y for x, y in zip(xs, ys)) / walkers)
    return out


if __name__ == "__main__":
    w = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    sd = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    data = msd(w, n, sd)
    for t in range(n // 10 - 1, n, n // 10):
        bar = "#" * int(data[t] / n * 40)
        print(f"t={t + 1:4d} msd={data[t]:8.1f} {bar}")
    print(f"slope ~ {data[-1] / n:.3f} (theory 1.0)")
