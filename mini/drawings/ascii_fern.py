"""Barnsley's fern in ASCII, grown by the chaos game on four affine maps (an iterated
function system). Denser cells get heavier characters.

    python ascii_fern.py            # the classic fern
    python ascii_fern.py --mutant   # a "Cyclosorus" mutant with different coefficients
"""
import random
import sys

W, H = 60, 40
SHADES = " .:-=+*#%@"

# (a, b, c, d, e, f, probability): x' = a x + b y + e,  y' = c x + d y + f
CLASSIC = (
    (0.00, 0.00, 0.00, 0.16, 0.0, 0.00, 0.01),
    (0.85, 0.04, -0.04, 0.85, 0.0, 1.60, 0.85),
    (0.20, -0.26, 0.23, 0.22, 0.0, 1.60, 0.07),
    (-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07),
)
MUTANT = (
    (0.00, 0.00, 0.00, 0.25, 0.0, -0.4, 0.02),
    (0.95, 0.005, -0.005, 0.93, -0.002, 0.5, 0.84),
    (0.035, -0.2, 0.16, 0.04, -0.09, 0.02, 0.07),
    (-0.04, 0.2, 0.16, 0.04, 0.083, 0.12, 0.07),
)


def fern(maps=CLASSIC, points: int = 120_000, seed: int = 1, w: int = W, h: int = H) -> list[str]:
    """Run the chaos game and return the density picture as text rows."""
    rng = random.Random(seed)
    weights = [m[6] for m in maps]
    x = y = 0.0
    pts = []
    for i in range(points):
        a, b, c, d, e, f, _ = rng.choices(maps, weights)[0]
        x, y = a * x + b * y + e, c * x + d * y + f
        if i > 20:
            pts.append((x, y))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    grid = [[0] * w for _ in range(h)]
    for px, py in pts:
        col = int((px - x0) / (x1 - x0 + 1e-12) * (w - 1))
        row = int((y1 - py) / (y1 - y0 + 1e-12) * (h - 1))
        grid[row][col] += 1
    top = max(max(r) for r in grid) or 1
    out = []
    for r in grid:
        line = ""
        for n in r:
            line += SHADES[0] if n == 0 else SHADES[min(len(SHADES) - 1, 1 + int((n / top) ** 0.35 * (len(SHADES) - 2)))]
        out.append(line.rstrip())
    return out


if __name__ == "__main__":
    mutant = "--mutant" in sys.argv
    print("\n".join(fern(MUTANT if mutant else CLASSIC)))
    print("Barnsley fern" + (" (mutant)" if mutant else "") + " — 120 000 chaos-game points")
