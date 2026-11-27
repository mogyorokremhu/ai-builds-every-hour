"""2D Ising model (Metropolis) on a torus. Usage: python ising_model.py [size] [temperature] [sweeps] [seed]
Below T_c ~ 2.269 spins align (|magnetisation| near 1); above it they disorder."""
import math
import random
import sys


def simulate(size: int = 24, temp: float = 2.0, sweeps: int = 200, seed: int = 1) -> tuple[float, float]:
    """Return (|magnetisation| per spin, energy per spin) after the given sweeps."""
    rng = random.Random(seed)
    s = [[1] * size for _ in range(size)]
    for _ in range(sweeps):
        for _ in range(size * size):
            i, j = rng.randrange(size), rng.randrange(size)
            nb = s[(i + 1) % size][j] + s[(i - 1) % size][j] + s[i][(j + 1) % size] + s[i][(j - 1) % size]
            dE = 2 * s[i][j] * nb
            if dE <= 0 or rng.random() < math.exp(-dE / temp):
                s[i][j] = -s[i][j]
    n = size * size
    mag = abs(sum(map(sum, s))) / n
    e = -sum(s[i][j] * (s[(i + 1) % size][j] + s[i][(j + 1) % size]) for i in range(size) for j in range(size)) / n
    return mag, e


if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    temps = [float(sys.argv[2])] if len(sys.argv) > 2 else [1.5, 2.0, 2.3, 2.6, 3.5]
    sweeps = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    sd = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    for t in temps:
        m, e = simulate(size, t, sweeps, sd)
        print(f"T={t:4.2f} |m|={m:5.3f} E/N={e:6.3f} {'#' * int(m * 30)}")
