#!/usr/bin/env python3
"""pct - percentile of numbers from stdin/files: `pct.py 50 90 99 [file]`. `--selftest` runs checks."""
import sys

def percentile(xs, p):
    """Linear-interpolated percentile (p in 0..100) of a non-empty list."""
    s = sorted(xs)
    k = (len(s) - 1) * p / 100
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)

def main(argv):
    ps = [float(a) for a in argv if a.replace(".", "", 1).isdigit()]
    files = [a for a in argv if not a.replace(".", "", 1).isdigit()]
    text = "".join(open(f).read() for f in files) if files else sys.stdin.read()
    xs = [float(t) for t in text.replace(",", " ").split()]
    if not xs or not ps:
        sys.exit("usage: pct.py P [P...] [file]  (numbers on stdin)")
    for p in ps:
        print(f"p{p:g}: {percentile(xs, p):g}")

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        assert percentile([1, 2, 3, 4], 50) == 2.5
        assert percentile([5], 99) == 5
        assert percentile([1, 2, 3, 4, 5], 100) == 5
        print("ok")
    else:
        main(sys.argv[1:])
