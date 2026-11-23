"""Burrows-Wheeler transform: groups similar characters, helping RLE."""


def bwt(s: str, end: str = "\0") -> str:
    s += end
    rots = sorted(s[i:] + s[:i] for i in range(len(s)))
    return "".join(r[-1] for r in rots)


def ibwt(t: str, end: str = "\0") -> str:
    table = [""] * len(t)
    for _ in range(len(t)):
        table = sorted(t[i] + table[i] for i in range(len(t)))
    return next(r for r in table if r.endswith(end))[:-1]


if __name__ == "__main__":
    text = "banana_bandana"
    t = bwt(text)
    print(repr(t))
    assert ibwt(t) == text
    print("round trip ok")
