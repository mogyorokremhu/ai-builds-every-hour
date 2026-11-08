#!/usr/bin/env python3
"""histo: text histogram of numbers from stdin/files. Usage: histo.py [-b BINS] [files]"""
import sys

def histogram(nums, bins=10):
    lo, hi = min(nums), max(nums)
    width = (hi - lo) / bins or 1
    counts = [0] * bins
    for n in nums:
        counts[min(int((n - lo) / width), bins - 1)] += 1
    return [(lo + i * width, lo + (i + 1) * width, c) for i, c in enumerate(counts)]

def render(rows, cols=40):
    top = max(c for _, _, c in rows) or 1
    return "\n".join(f"{a:10.3g} - {b:10.3g} | {'#' * round(c / top * cols):<{cols}} {c}" for a, b, c in rows)

if __name__ == "__main__":
    args = sys.argv[1:]
    bins = 10
    if "-b" in args:
        i = args.index("-b"); bins = int(args[i + 1]); del args[i:i + 2]
    assert sum(c for *_, c in histogram([1, 2, 3, 4, 5, 5], 5)) == 6
    data = "".join(open(f).read() for f in args) if args else sys.stdin.read()
    nums = [float(t) for t in data.split()]
    print(render(histogram(nums, bins)) if nums else "no numbers")
