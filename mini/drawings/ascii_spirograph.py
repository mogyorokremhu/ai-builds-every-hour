"""Spirograph curves (hypotrochoids and epitrochoids) plotted in ASCII. The curve closes
after R / gcd(R, r) turns of the small wheel.

    python ascii_spirograph.py                 # a gallery of four
    python ascii_spirograph.py 96 36 30        # hypotrochoid: ring R, wheel r, pen d
    python ascii_spirograph.py 60 20 30 --epi  # epitrochoid (wheel rolling outside)
"""
import math
import sys

W, H = 72, 34
GALLERY = ((96, 36, 30, False), (105, 30, 45, False), (60, 23, 40, False), (50, 15, 25, True))


def curve(R: int, r: int, d: float, epi: bool = False, steps_per_turn: int = 720) -> list[tuple[float, float]]:
    """Points of the closed curve."""
    turns = r // math.gcd(R, r)
    n = turns * steps_per_turn
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * turns * i / n
        if epi:
            x = (R + r) * math.cos(t) - d * math.cos((R + r) / r * t)
            y = (R + r) * math.sin(t) - d * math.sin((R + r) / r * t)
        else:
            x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
            y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
        pts.append((x, y))
    return pts


def plot(pts: list[tuple[float, float]], w: int = W, h: int = H) -> list[str]:
    """Rasterise points; cells the pen crosses often get heavier marks."""
    span = max(max(abs(x) for x, _ in pts), max(abs(y) for _, y in pts)) or 1
    grid = [[0] * w for _ in range(h)]
    for x, y in pts:
        col = int((x / span + 1) / 2 * (w - 1))
        row = int((1 - (y / span + 1) / 2) * (h - 1))
        grid[row][col] += 1
    marks = " .o*O@"
    top = max(max(r) for r in grid)
    return ["".join(marks[0] if n == 0 else marks[min(5, 1 + int(4 * n / top))] for n in r).rstrip() for r in grid]


def main(argv: list[str]) -> None:
    """Print the requested curve or the gallery."""
    nums = [a for a in argv if not a.startswith("--")]
    specs = [(int(nums[0]), int(nums[1]), float(nums[2]), "--epi" in argv)] if len(nums) >= 3 else GALLERY
    for R, r, d, epi in specs:
        print("\n".join(plot(curve(R, r, d, epi))))
        print(f"{'epi' if epi else 'hypo'}trochoid R={R} r={r} d={d:g}\n")


if __name__ == "__main__":
    main(sys.argv[1:])
