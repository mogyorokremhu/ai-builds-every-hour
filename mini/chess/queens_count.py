"""Count N-queens solutions (total and distinct up to rotation/reflection)."""
import sys


def solutions(n: int):
    cols, d1, d2, cur, out = set(), set(), set(), [], []

    def go(r: int):
        if r == n:
            out.append(tuple(cur))
            return
        for c in range(n):
            if c in cols or r - c in d1 or r + c in d2:
                continue
            cols.add(c); d1.add(r - c); d2.add(r + c); cur.append(c)
            go(r + 1)
            cols.remove(c); d1.remove(r - c); d2.remove(r + c); cur.pop()

    go(0)
    return out


def transforms(sol):
    n = len(sol)
    cells = [(r, c) for r, c in enumerate(sol)]
    res = []
    for _ in range(4):
        cells = [(c, n - 1 - r) for r, c in cells]  # rotate 90
        for cs in (cells, [(r, n - 1 - c) for r, c in cells]):
            res.append(tuple(c for _, c in sorted(cs)))
    return res


def distinct(sols):
    seen = set()
    count = 0
    for s in sols:
        if s in seen:
            continue
        count += 1
        seen.update(transforms(s))
    return count


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    s = solutions(n)
    print(f"n={n}: {len(s)} total, {distinct(s)} distinct")
