"""Two-colour Game of Life duel: births take the majority colour of the neighbours.
Prints which colour owns more cells after N generations. `--auto` is the default run."""
import random
import sys

W, H, GENS = 30, 14, 60


def step(g):
    n = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            nb = [g[(y + dy) % H][(x + dx) % W] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy]
            live = [v for v in nb if v]
            if g[y][x] and len(live) in (2, 3):
                n[y][x] = g[y][x]
            elif not g[y][x] and len(live) == 3:
                n[y][x] = 1 if live.count(1) > live.count(2) else 2
    return n


def main() -> None:
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 7)
    g = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if random.random() < 0.3:
                g[y][x] = 1 if x < W // 2 else 2
    for _ in range(GENS):
        g = step(g)
    print("\n".join("".join(".#@"[v] for v in row) for row in g))
    a = sum(r.count(1) for r in g)
    b = sum(r.count(2) for r in g)
    print(f"# = {a}, @ = {b} -> {'#' if a > b else '@' if b > a else 'tie'}")


if __name__ == "__main__":
    main()
