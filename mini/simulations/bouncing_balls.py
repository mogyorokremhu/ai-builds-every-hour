"""Elastic balls bouncing in a box; prints energy conservation. Usage: python bouncing_balls.py [steps] [seed]"""
import random
import sys


def simulate(steps: int = 1000, n: int = 5, seed: int = 1, dt: float = 0.01):
    rng = random.Random(seed)
    balls = [[rng.uniform(1, 9), rng.uniform(1, 9), rng.uniform(-3, 3), rng.uniform(-3, 3)] for _ in range(n)]
    energy = lambda: sum(0.5 * (b[2] ** 2 + b[3] ** 2) for b in balls)
    e0 = energy()
    for _ in range(steps):
        for b in balls:
            b[0] += b[2] * dt
            b[1] += b[3] * dt
            if not 0 < b[0] < 10:
                b[2] = -b[2]
            if not 0 < b[1] < 10:
                b[3] = -b[3]
    return e0, energy(), balls


if __name__ == "__main__":
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    e0, e1, balls = simulate(steps, seed=seed)
    print(f"energy before {e0:.4f}, after {e1:.4f}")
    for i, b in enumerate(balls):
        print(f"ball {i}: x={b[0]:.2f} y={b[1]:.2f}")
