#!/usr/bin/env python3
"""Summary statistics for numbers from files/stdin: count, mean, median, stdev, quartiles."""
import statistics as st, sys

def summarize(xs):
    xs = sorted(xs)
    q = st.quantiles(xs, n=4) if len(xs) > 1 else [xs[0]] * 3
    return {"n": len(xs), "min": xs[0], "q1": q[0], "median": st.median(xs), "q3": q[2],
            "max": xs[-1], "mean": st.fmean(xs), "stdev": st.stdev(xs) if len(xs) > 1 else 0.0}

def main(argv):
    text = open(argv[0]).read() if argv else sys.stdin.read()
    xs = [float(t) for t in text.replace(",", " ").split()]
    if not xs:
        sys.exit("no numbers")
    for k, v in summarize(xs).items():
        print(f"{k:>7}: {v:g}")

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        s = summarize([1, 2, 3, 4, 5]); assert s["median"] == 3 and s["mean"] == 3 and s["n"] == 5; print("ok")
    else:
        main(sys.argv[1:])
