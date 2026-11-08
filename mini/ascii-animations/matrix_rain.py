#!/usr/bin/env python3
"""Falling green character columns. Usage: matrix_rain.py [frames] [width] [height]"""
import random, sys, time

def main():
    frames = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    w = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    h = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    rnd = random.Random(7)
    heads = [rnd.randint(-h, 0) for _ in range(w)]
    trail = [rnd.randint(4, 9) for _ in range(w)]
    chars = "01ABCDEFabcdef$#@%&*+="
    for _ in range(frames):
        rows = []
        for y in range(h):
            row = ""
            for x in range(w):
                d = heads[x] - y
                row += (rnd.choice(chars) if 0 <= d < trail[x] else " ")
            rows.append(row)
        print("\033[H\033[32m" + "\n".join(rows) + "\033[0m")
        heads = [(hd + 1) if hd - trail[i] < h else rnd.randint(-h // 2, 0) for i, hd in enumerate(heads)]
        time.sleep(0.06)

if __name__ == "__main__":
    main()
