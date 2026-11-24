"""Run-length compression of L-system strings: how much does each generation shrink?"""
from itertools import groupby

RULES = {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}


def rle(s: str) -> str:
    return "".join(c if n == 1 else f"{c}{n}" for c, n in ((k, len(list(g))) for k, g in groupby(s)))


def unrle(s: str) -> str:
    out, i = [], 0
    while i < len(s):
        c = s[i]
        i += 1
        j = i
        while j < len(s) and s[j].isdigit():
            j += 1
        out.append(c * (int(s[i:j]) if j > i else 1))
        i = j
    return "".join(out)


if __name__ == "__main__":
    s = "X"
    print("gen  length  rle-length  ratio")
    for g in range(0, 6):
        r = rle(s)
        assert unrle(r) == s
        print(f"{g:>3} {len(s):>7} {len(r):>11} {len(r) / len(s):>6.2f}")
        s = "".join(RULES.get(c, c) for c in s)
