#!/usr/bin/env python3
"""rush_hour_lite - Rush Hour sliding-car puzzle solver (BFS, fewest moves) on a 6x6 board.

Board: 36 chars, '.' empty, same letter = one car, 'X' = the red car (row 2, horizontal).
  python3 rush_hour_lite.py            solves the built-in sample
"""
from collections import deque

SAMPLE = "AAB.....B.C..XX.C..................."


def cars(board):
    pos = {}
    for i, c in enumerate(board):
        if c != ".":
            pos.setdefault(c, []).append(i)
    return pos


def moves(board):
    for c, cells in cars(board).items():
        step = 1 if cells[1] - cells[0] == 1 else 6
        lo, hi = cells[0], cells[-1]
        for d in (-1, 1):
            n = 0
            while True:
                n += 1
                nxt = (lo - step * n) if d < 0 else (hi + step * n)
                if not 0 <= nxt < 36 or (step == 1 and nxt // 6 != lo // 6) or board[nxt] != ".":
                    break
                b = list(board)
                for x in cells:
                    b[x] = "."
                for x in cells:
                    b[x + d * step * n] = c
                yield "".join(b), (c, d * n)


def solve(board):
    seen = {board: None}
    q = deque([board])
    while q:
        b = q.popleft()
        if b[16] == "X" and b[17] == "X":
            path = []
            while seen[b]:
                b, mv = seen[b]
                path.append(mv)
            return path[::-1]
        for nb, mv in moves(b):
            if nb not in seen:
                seen[nb] = (b, mv)
                q.append(nb)


if __name__ == "__main__":
    s = solve(SAMPLE)
    print(f"{len(s)} moves:" if s is not None else "no solution", s)
