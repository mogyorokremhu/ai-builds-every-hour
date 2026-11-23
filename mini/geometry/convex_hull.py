"""Convex hull (Andrew's monotone chain) with a self-check. Usage: python convex_hull.py"""
import random


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


if __name__ == "__main__":
    random.seed(1)
    pts = [(random.randint(0, 20), random.randint(0, 20)) for _ in range(40)]
    h = hull(pts)
    print("hull:", h)
    n = len(h)
    assert all(cross(h[i], h[(i + 1) % n], p) >= 0 for i in range(n) for p in pts)
    print("ok: every point is on the left of every hull edge")
