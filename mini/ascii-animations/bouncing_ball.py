#!/usr/bin/env python3
"""A ball bouncing with gravity and a fading trail. Usage: bouncing_ball.py [frames]"""
import sys, time

W, H = 40, 14

def main():
    frames = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    x, y, vx, vy = 2.0, 1.0, 0.7, 0.0
    trail = []
    for _ in range(frames):
        vy += 0.12
        x += vx; y += vy
        if x < 0 or x > W - 1: vx = -vx; x = max(0, min(W - 1, x))
        if y > H - 1: y = H - 1; vy = -vy * 0.88
        trail.append((int(x), int(y)))
        trail = trail[-6:]
        grid = [[" "] * W for _ in range(H)]
        for i, (tx, ty) in enumerate(trail[:-1]):
            grid[ty][tx] = ".:"[i > 2]
        bx, by = trail[-1]
        grid[by][bx] = "O"
        print("\033[H" + "\n".join("".join(r) for r in grid) + "\n" + "=" * W)
        time.sleep(0.04)

if __name__ == "__main__":
    main()
