"""Bridge-and-torch puzzle: minimal total crossing time for any group of walkers."""
import sys


def min_time(times):
    t = sorted(times)
    total = 0
    while len(t) > 3:
        # either fastest shuttles, or two fastest escort the two slowest
        total += min(t[0] + 2 * t[1] + t[-1], 2 * t[0] + t[-2] + t[-1])
        t = t[:-2]
    if len(t) == 3:
        return total + t[0] + t[1] + t[2]
    if len(t) == 2:
        return total + t[1]
    return total + (t[0] if t else 0)


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:]] or [1, 2, 5, 10]
    print(f"crossing times {args} -> minimum total {min_time(args)}")
