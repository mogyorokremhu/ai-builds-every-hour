#!/usr/bin/env python3
"""Deterministic lorem-ipsum generator: lorem.py [-p PARAGRAPHS] [-s SEED]"""
import argparse, random
WORDS = ("lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor "
         "incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud").split()

def sentence(rng):
    w = [rng.choice(WORDS) for _ in range(rng.randint(6, 14))]
    return w[0].capitalize() + " " + " ".join(w[1:]) + "."

def paragraph(rng):
    return " ".join(sentence(rng) for _ in range(rng.randint(3, 6)))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", type=int, default=2)
    ap.add_argument("-s", type=int, default=1)
    a = ap.parse_args()
    rng = random.Random(a.s)
    print("\n\n".join(paragraph(rng) for _ in range(a.p)))
