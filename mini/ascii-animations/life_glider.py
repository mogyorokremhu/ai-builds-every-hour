#!/usr/bin/env python3
"""Conway's Life on a torus with a glider and a blinker. Usage: life_glider.py [generations]"""
import sys, time

W, H = 32, 14

def step(cells):
    counts = {}
    for (x, y) in cells:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy:
                    k = ((x + dx) % W, (y + dy) % H)
                    counts[k] = counts.get(k, 0) + 1
    return {c for c, n in counts.items() if n == 3 or (n == 2 and c in cells)}

def main():
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    cells = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2), (20, 8), (21, 8), (22, 8)}
    for g in range(gens):
        rows = ["".join("#" if (x, y) in cells else "." for x in range(W)) for y in range(H)]
        print("\033[H" + "\n".join(rows) + f"\ngen {g}")
        cells = step(cells)
        time.sleep(0.08)

if __name__ == "__main__":
    main()
