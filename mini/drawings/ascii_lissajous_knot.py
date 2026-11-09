"""Trefoil-style knot projection with depth shading. python ascii_lissajous_knot.py"""
import math


def main(w: int = 70, h: int = 34, steps: int = 4000) -> None:
    grid = [[" "] * w for _ in range(h)]
    depth = [[-9.0] * w for _ in range(h)]
    for i in range(steps):
        t = 2 * math.pi * i / steps
        x = math.sin(t) + 2 * math.sin(2 * t)
        y = math.cos(t) - 2 * math.cos(2 * t)
        z = -math.sin(3 * t)
        cx, cy = int(w / 2 + x * w / 7), int(h / 2 + y * h / 7)
        if 0 <= cx < w and 0 <= cy < h and z > depth[cy][cx]:
            depth[cy][cx] = z
            grid[cy][cx] = ".:+#"[min(3, int((z + 1) * 2))]
    print("\n".join("".join(r).rstrip() for r in grid))


if __name__ == "__main__":
    main()
