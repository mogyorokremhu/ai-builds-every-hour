"""A Penrose rhombus tiling (P3) in ASCII, made by repeatedly subdividing Robinson
triangles around a "sun" of ten triangles. Thin rhombs are drawn with '.', thick ones
with '#', and tile edges are left blank so the pattern of rhombs shows.

    python ascii_penrose.py          # 5 subdivisions
    python ascii_penrose.py 6        # finer
"""
import cmath
import math
import sys

PHI = (1 + 5 ** 0.5) / 2
W, H = 78, 38


def sun() -> list[tuple[int, complex, complex, complex]]:
    """Ten thin-type (0) triangles in a wheel around the origin."""
    tris = []
    for i in range(10):
        b = cmath.rect(1, (2 * i - 1) * math.pi / 10)
        c = cmath.rect(1, (2 * i + 1) * math.pi / 10)
        if i % 2 == 0:
            b, c = c, b  # mirror every second triangle so the rhombs pair up
        tris.append((0, 0j, b, c))
    return tris


def subdivide(tris):
    """One deflation step of Robinson triangles (type 0 = half thin rhomb, 1 = half thick)."""
    out = []
    for kind, a, b, c in tris:
        if kind == 0:
            p = a + (b - a) / PHI
            out += [(0, c, p, b), (1, p, c, a)]
        else:
            q = b + (a - b) / PHI
            r = b + (c - b) / PHI
            out += [(1, r, c, a), (1, q, r, b), (0, r, q, a)]
    return out


def inside(p: complex, a: complex, b: complex, c: complex) -> float:
    """Smallest barycentric coordinate of p (negative = outside the triangle)."""
    d = (b.imag - c.imag) * (a.real - c.real) + (c.real - b.real) * (a.imag - c.imag)
    l1 = ((b.imag - c.imag) * (p.real - c.real) + (c.real - b.real) * (p.imag - c.imag)) / d
    l2 = ((c.imag - a.imag) * (p.real - c.real) + (a.real - c.real) * (p.imag - c.imag)) / d
    return min(l1, l2, 1 - l1 - l2)


def render(depth: int = 5, w: int = W, h: int = H) -> list[str]:
    """Rasterise the tiling into text rows."""
    tris = sun()
    for _ in range(depth):
        tris = subdivide(tris)
    grid = [[" "] * w for _ in range(h)]
    edge = 0.06 * (1.25 ** (depth - 5))  # thinner gaps at higher depth would vanish; keep them visible
    edge = min(0.2, max(0.04, edge * 1.0))
    for kind, a, b, c in tris:
        xs = [z.real for z in (a, b, c)]
        ys = [z.imag for z in (a, b, c)]
        c0 = max(0, int((min(xs) + 1) / 2 * (w - 1)))
        c1 = min(w - 1, int((max(xs) + 1) / 2 * (w - 1)) + 1)
        r0 = max(0, int((1 - max(ys)) / 2 * (h - 1)))
        r1 = min(h - 1, int((1 - min(ys)) / 2 * (h - 1)) + 1)
        for row in range(r0, r1 + 1):
            for col in range(c0, c1 + 1):
                p = complex(col / (w - 1) * 2 - 1, 1 - row / (h - 1) * 2)
                m = inside(p, a, b, c)
                if m >= 0:
                    # only the two outer edges (a-b and a-c) are rhomb edges; b-c is the shared diagonal
                    d = (b.imag - c.imag) * (a.real - c.real) + (c.real - b.real) * (a.imag - c.imag)
                    l_a = ((b.imag - c.imag) * (p.real - c.real) + (c.real - b.real) * (p.imag - c.imag)) / d
                    l_b = ((c.imag - a.imag) * (p.real - c.real) + (a.real - c.real) * (p.imag - c.imag)) / d
                    l_c = 1 - l_a - l_b
                    on_edge = min(l_b, l_c) < edge  # near edge a-c (l_b≈0) or a-b (l_c≈0)
                    grid[row][col] = " " if on_edge else (".#"[kind])
    return ["".join(r).rstrip() for r in grid]


if __name__ == "__main__":
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("\n".join(render(depth)))
    print(f"Penrose P3 tiling, {depth} subdivisions ('.' thin rhombs, '#' thick rhombs)")
