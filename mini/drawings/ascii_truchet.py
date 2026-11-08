"""Truchet tiles: every cell holds one of two rotations of the same tile, chosen at random,
and the pieces join into winding paths and loops.

    python ascii_truchet.py              # quarter-circle arcs that join into winding paths
    python ascii_truchet.py --diagonal   # the original diagonal tiles: ╱ ╲
    python ascii_truchet.py --seed 9 --size 50x20
"""
import random
import sys

TILE_W, TILE_H = 12, 6  # characters per tile (terminal cells are ~2× taller than wide)


def arcs(w: int, h: int, rng: random.Random) -> list[str]:
    """Quarter-circle Truchet pattern: each tile has two arcs of radius ½ centred on opposite
    corners (top-left + bottom-right, or top-right + bottom-left), rasterised into w×h tiles."""
    flips = [[rng.random() < 0.5 for _ in range(w)] for _ in range(h)]
    rows = []
    for y in range(h * TILE_H):
        line = []
        for x in range(w * TILE_W):
            tx, ty = x // TILE_W, y // TILE_H
            u = (x % TILE_W + 0.5) / TILE_W   # 0..1 across the tile
            v = (y % TILE_H + 0.5) / TILE_H
            corners = ((0, 0), (1, 1)) if flips[ty][tx] else ((1, 0), (0, 1))
            d = min(abs(((u - cx) ** 2 + (v - cy) ** 2) ** 0.5 - 0.5) for cx, cy in corners)
            line.append("@" if d < 0.05 else "o" if d < 0.1 else " ")
        rows.append("".join(line).rstrip())
    return rows


def diagonals(w: int, h: int, rng: random.Random) -> list[str]:
    """Smith's diagonal Truchet tiles, one character per tile."""
    return ["".join(rng.choice("╱╲") for _ in range(w)) for _ in range(h)]


def parse(argv: list[str]) -> tuple[int, int, int, bool]:
    """Read --seed, --size WxH and --diagonal from the command line."""
    seed, w, h = random.randrange(10**6), 6, 5
    if "--seed" in argv:
        seed = int(argv[argv.index("--seed") + 1])
    if "--size" in argv:
        w, h = map(int, argv[argv.index("--size") + 1].lower().split("x"))
    return seed, w, h, "--diagonal" in argv


def main(argv: list[str]) -> None:
    """Print a pattern."""
    seed, w, h, diag = parse(argv)
    rng = random.Random(seed)
    rows = diagonals(w * 12, h * 6, rng) if diag else arcs(w, h, rng)
    print("\n".join(rows))
    print(f"Truchet {'diagonal' if diag else 'arc'} tiling, seed {seed}")


if __name__ == "__main__":
    main(sys.argv[1:])
