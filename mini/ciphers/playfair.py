"""Playfair digraph cipher (I/J merged). Usage: python playfair.py KEY [-d] text..."""
import sys


def square(key: str) -> list[str]:
    seen: list[str] = []
    for c in (key.upper() + "ABCDEFGHIKLMNOPQRSTUVWXYZ").replace("J", "I"):
        if c.isalpha() and c not in seen:
            seen.append(c)
    return seen


def _pairs(text: str) -> list[str]:
    t = [c for c in text.upper().replace("J", "I") if c.isalpha()]
    out, i = [], 0
    while i < len(t):
        a = t[i]
        b = t[i + 1] if i + 1 < len(t) else "X"
        if a == b:
            out.append(a + "X"); i += 1
        else:
            out.append(a + b); i += 2
    return out


def crypt(key: str, text: str, decrypt: bool = False) -> str:
    sq = square(key)
    pos = {c: divmod(i, 5) for i, c in enumerate(sq)}
    d = -1 if decrypt else 1
    res = []
    for p in (_pairs(text) if not decrypt else [text[i:i + 2] for i in range(0, len(text), 2)]):
        (r1, c1), (r2, c2) = pos[p[0]], pos[p[1]]
        if r1 == r2:
            c1, c2 = (c1 + d) % 5, (c2 + d) % 5
        elif c1 == c2:
            r1, r2 = (r1 + d) % 5, (r2 + d) % 5
        else:
            c1, c2 = c2, c1
        res.append(sq[r1 * 5 + c1] + sq[r2 * 5 + c2])
    return "".join(res)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) >= 2:
        dec = "-d" in args
        rest = [a for a in args if a != "-d"]
        print(crypt(rest[0], "".join(rest[1:]), dec))
    else:
        c = crypt("PLAYFAIR EXAMPLE", "HIDE THE GOLD IN THE TREE STUMP")
        print(c)
        assert c == "BMODZBXDNABEKUDMUIXMMOUVIF", c
        print(crypt("PLAYFAIR EXAMPLE", c, True))
