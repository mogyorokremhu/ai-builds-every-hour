"""Golden (Fibonacci) spiral: quarter-circle arcs through Fibonacci squares.

Usage: python golden_spiral_ascii.py [turns]   (default 8 quarter arcs)
"""
import math
import sys


def fib_squares(n):
    a, b = 1, 1
    out = []
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out


def spiral_points(n):
    """Points along quarter-circle arcs of radius F_k, each arc turning 90 degrees."""
    cx, cy = 0.0, 0.0
    heading = 0.0          # direction of the arc's starting tangent
    x, y = 0.0, 0.0
    pts = []
    for r in fib_squares(n):
        # centre is perpendicular (left) of current heading
        cx, cy = x - r * math.sin(heading), y + r * math.cos(heading)
        start = heading - math.pi / 2
        for i in range(31):
            a = start + (math.pi / 2) * i / 30
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        x, y = pts[-1]
        heading += math.pi / 2
    return pts


def render(n=8, width=72, height=36):
    pts = spiral_points(n)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    grid = [[" "] * width for _ in range(height)]
    for x, y in pts:
        c = int((x - x0) / (x1 - x0) * (width - 1))
        r = int((1 - (y - y0) / (y1 - y0)) * (height - 1))
        grid[r][c] = "o"
    return "\n".join("".join(row).rstrip() for row in grid)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    print(render(n))
    print("squares:", fib_squares(n))
