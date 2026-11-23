"""Smallest enclosing circle (Welzl-style, iterative). Usage: python minimum_enclosing_circle.py"""
import math
import random


def _circle2(a, b):
    c = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    return c, math.dist(a, b) / 2


def _circle3(a, b, c):
    d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    if d == 0:
        return max((_circle2(a, b), _circle2(a, c), _circle2(b, c)), key=lambda t: t[1])
    s = [p[0] ** 2 + p[1] ** 2 for p in (a, b, c)]
    ux = (s[0] * (b[1] - c[1]) + s[1] * (c[1] - a[1]) + s[2] * (a[1] - b[1])) / d
    uy = (s[0] * (c[0] - b[0]) + s[1] * (a[0] - c[0]) + s[2] * (b[0] - a[0])) / d
    return (ux, uy), math.dist((ux, uy), a)


def _in(circ, p):
    return math.dist(circ[0], p) <= circ[1] + 1e-9


def enclosing_circle(points):
    pts = list(points)
    random.Random(0).shuffle(pts)
    circ = (pts[0], 0.0)
    for i, p in enumerate(pts):
        if _in(circ, p):
            continue
        circ = (p, 0.0)
        for j in range(i):
            if _in(circ, pts[j]):
                continue
            circ = _circle2(p, pts[j])
            for k in range(j):
                if not _in(circ, pts[k]):
                    circ = _circle3(p, pts[j], pts[k])
    return circ


if __name__ == "__main__":
    random.seed(3)
    pts = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(100)]
    c, r = enclosing_circle(pts)
    assert all(math.dist(c, p) <= r + 1e-9 for p in pts)
    print(f"centre=({c[0]:.3f}, {c[1]:.3f}) radius={r:.3f} encloses all {len(pts)} points")
