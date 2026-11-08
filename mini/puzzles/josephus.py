#!/usr/bin/env python3
"""Josephus problem: n people in a circle, every k-th is eliminated. Who survives?

usage: josephus.py N K          survivor (1-based) plus the elimination order
       josephus.py --table N    survivors for k=2..9
"""
import sys


def survivor(n, k):
    pos = 0
    for m in range(2, n + 1):
        pos = (pos + k) % m
    return pos + 1


def order(n, k):
    people = list(range(1, n + 1))
    out, i = [], 0
    while people:
        i = (i + k - 1) % len(people)
        out.append(people.pop(i))
    return out


def main(argv):
    if argv and argv[0] == "--table":
        n = int(argv[1])
        print(" ".join(f"k={k}:{survivor(n, k)}" for k in range(2, 10)))
        return
    n, k = int(argv[0]), int(argv[1])
    seq = order(n, k)
    assert seq[-1] == survivor(n, k)
    print(f"survivor: {seq[-1]}")
    print("order:", " ".join(map(str, seq)))


if __name__ == "__main__":
    main(sys.argv[1:] or ["41", "3"])
