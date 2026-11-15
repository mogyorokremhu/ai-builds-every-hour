"""Rose curves r = cos(k*theta) written to an SVG file.

Usage: python rose_curve_svg.py [n d out.svg]   (k = n/d, default 5 3 rose.svg)
"""
import math
import sys


def rose_points(n: int = 5, d: int = 3, steps: int = 3000, size: int = 200):
    """Points of r = cos(n/d * theta) scaled to an SVG viewbox."""
    turns = d * 2 if (n * d) % 2 == 0 else d
    pts = []
    for i in range(steps + 1):
        t = math.pi * turns * i / steps
        r = math.cos(n / d * t)
        pts.append((size + size * 0.9 * r * math.cos(t), size - size * 0.9 * r * math.sin(t)))
    return pts


def to_svg(n: int = 5, d: int = 3) -> str:
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in rose_points(n, d))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">'
            f'<rect width="400" height="400" fill="#101020"/>'
            f'<polyline fill="none" stroke="#ff7ab8" stroke-width="1.2" points="{pts}"/></svg>')


if __name__ == "__main__":
    a = sys.argv[1:]
    n, d = (int(a[0]), int(a[1])) if len(a) >= 2 else (5, 3)
    out = a[2] if len(a) >= 3 else "rose.svg"
    with open(out, "w") as f:
        f.write(to_svg(n, d))
    print(f"wrote {out} (k={n}/{d})")
