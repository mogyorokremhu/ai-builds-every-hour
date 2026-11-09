"""Sum/avg/min/max of a numeric column: python colsum.py COL [-d SEP] < file  (COL is 1-based)."""
import sys


def column(lines, col, sep=None):
    vals = []
    for ln in lines:
        parts = ln.split(sep) if sep else ln.split()
        try:
            vals.append(float(parts[col - 1]))
        except (IndexError, ValueError):
            pass
    return vals


def summary(vals):
    if not vals:
        return "no numbers"
    return f"n={len(vals)} sum={sum(vals):g} avg={sum(vals)/len(vals):g} min={min(vals):g} max={max(vals):g}"


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert column(["a 1", "b 2.5", "c x"], 2) == [1.0, 2.5]
        assert summary([1, 3]) == "n=2 sum=4 avg=2 min=1 max=3"
        print("ok")
        sys.exit()
    a = sys.argv[1:]
    sep = a[a.index("-d") + 1] if "-d" in a else None
    print(summary(column(sys.stdin, int(a[0]), sep)))
