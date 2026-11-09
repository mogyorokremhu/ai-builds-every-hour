"""Heighway dragon curve on a character grid.  python ascii_dragon_curve.py [order]"""
import sys

def turns(order):
    t = []
    for _ in range(order):
        t = t + [1] + [-x for x in reversed(t)]
    return t

def main(order=9):
    x = y = 0
    dx, dy = 1, 0
    pts = {(0, 0)}
    for t in turns(order):
        x, y = x + dx, y + dy
        pts.add((x, y))
        dx, dy = (-dy, dx) if t == 1 else (dy, -dx)
        x, y = x + dx, y + dy
        pts.add((x, y))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    for r in range(min(ys), max(ys) + 1):
        print("".join("#" if (c, r) in pts else " " for c in range(min(xs), max(xs) + 1)).rstrip())

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 9)
