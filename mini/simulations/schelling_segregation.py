"""Schelling segregation model on a torus. Usage: python schelling_segregation.py [size] [tolerance] [seed]
Agents move to a random empty cell when fewer than `tolerance` of their neighbours share their type."""
import random
import sys


def similarity(grid: list[list[int]]) -> float:
    """Average fraction of same-type neighbours over all agents."""
    n = len(grid)
    tot = cnt = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                continue
            same = occ = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di or dj:
                        v = grid[(i + di) % n][(j + dj) % n]
                        if v:
                            occ += 1
                            same += v == grid[i][j]
            if occ:
                tot += same / occ
                cnt += 1
    return tot / cnt if cnt else 0.0


def simulate(size: int = 20, tol: float = 0.4, seed: int = 1, rounds: int = 60) -> tuple[list[list[int]], float, float]:
    """Return (final grid, initial similarity, final similarity)."""
    rng = random.Random(seed)
    cells = [1] * int(size * size * 0.45) + [2] * int(size * size * 0.45)
    cells += [0] * (size * size - len(cells))
    rng.shuffle(cells)
    grid = [cells[i * size:(i + 1) * size] for i in range(size)]
    start = similarity(grid)
    for _ in range(rounds):
        moved = 0
        empties = [(i, j) for i in range(size) for j in range(size) if grid[i][j] == 0]
        agents = [(i, j) for i in range(size) for j in range(size) if grid[i][j]]
        rng.shuffle(agents)
        for i, j in agents:
            same = occ = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di or dj:
                        v = grid[(i + di) % size][(j + dj) % size]
                        if v:
                            occ += 1
                            same += v == grid[i][j]
            if occ and same / occ < tol:
                k = rng.randrange(len(empties))
                ei, ej = empties[k]
                grid[ei][ej], grid[i][j] = grid[i][j], 0
                empties[k] = (i, j)
                moved += 1
        if moved == 0:
            break
    return grid, start, similarity(grid)


if __name__ == "__main__":
    sz = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 0.4
    sd = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    g, a, b = simulate(sz, tl, sd)
    for row in g:
        print("".join(" XO"[v] for v in row))
    print(f"similarity {a:.2f} -> {b:.2f} (tolerance {tl})")
