"""Triangle centers: centroid, circumcenter, incenter, orthocenter. Usage: python triangle_centers.py"""
import math


def centers(a, b, c):
    (ax, ay), (bx, by), (cx, cy) = a, b, c
    centroid = ((ax + bx + cx) / 3, (ay + by + cy) / 3)
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    circum = (ux, uy)
    la, lb, lc = math.dist(b, c), math.dist(a, c), math.dist(a, b)
    p = la + lb + lc
    incenter = ((la * ax + lb * bx + lc * cx) / p, (la * ay + lb * by + lc * cy) / p)
    ortho = (3 * centroid[0] - 2 * ux, 3 * centroid[1] - 2 * uy)  # Euler line: H = 3G - 2O
    return centroid, circum, incenter, ortho


if __name__ == "__main__":
    for name, pt in zip(("centroid", "circumcenter", "incenter", "orthocenter"), centers((0, 0), (4, 0), (0, 3))):
        print(f"{name:13} ({pt[0]:.3f}, {pt[1]:.3f})")
    g, o, _, h = centers((0, 0), (5, 1), (2, 6))
    assert abs((h[0] - g[0]) - 2 * (g[0] - o[0])) < 1e-9
    print("Euler line check ok")
