"""Nagel-Schreckenberg traffic model on a ring road. Usage: python traffic_nasch.py [cars] [steps] [seed]"""
import random
import sys


def step(pos: list[int], vel: list[int], length: int, vmax: int, p: float, rng: random.Random) -> None:
    """Advance one tick: accelerate, brake to gap, random slowdown, move."""
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i])
    for k, i in enumerate(order):
        ahead = order[(k + 1) % n]
        gap = (pos[ahead] - pos[i] - 1) % length if n > 1 else length
        v = min(vel[i] + 1, vmax, gap)
        if v > 0 and rng.random() < p:
            v -= 1
        vel[i] = v
    for i in range(n):
        pos[i] = (pos[i] + vel[i]) % length


def run(cars: int = 20, steps: int = 20, length: int = 70, vmax: int = 5, p: float = 0.3, seed: int = 1) -> list[str]:
    rng = random.Random(seed)
    pos = rng.sample(range(length), cars)
    vel = [0] * cars
    rows = []
    for _ in range(steps):
        road = ["."] * length
        for i in range(cars):
            road[pos[i]] = str(vel[i])
        rows.append("".join(road))
        step(pos, vel, length, vmax, p, rng)
    flow = sum(vel) / length
    rows.append(f"density {cars / length:.2f}  final flow {flow:.3f} cars/cell/tick")
    return rows


if __name__ == "__main__":
    c = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    s = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    sd = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    print("\n".join(run(c, s, seed=sd)))
