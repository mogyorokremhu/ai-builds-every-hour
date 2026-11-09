#!/usr/bin/env python3
"""Count regex matches per file: grepc.py PATTERN FILE... [-i]"""
import argparse, re
ap = argparse.ArgumentParser()
ap.add_argument("pattern"); ap.add_argument("files", nargs="+"); ap.add_argument("-i", action="store_true")
a = ap.parse_args()
rx = re.compile(a.pattern, re.I if a.i else 0)
for f in a.files:
    try:
        n = sum(len(rx.findall(line)) for line in open(f, errors="replace"))
    except OSError as e:
        print(f"{f}: {e}"); continue
    print(f"{n:6d}  {f}")
