"""Homophonic substitution: frequent letters get several numeric symbols, used in rotation.
Usage: python homophonic.py "text" """
import sys

FREQ = {"E": 4, "T": 3, "A": 3, "O": 3, "N": 2, "I": 2, "S": 2, "R": 2, "H": 2}


def build_table() -> dict[str, list[str]]:
    table: dict[str, list[str]] = {}
    n = 10
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        k = FREQ.get(ch, 1)
        table[ch] = [f"{n + j:02d}" for j in range(k)]
        n += k
    return table


def encrypt(text: str) -> str:
    table = build_table()
    counters = {c: 0 for c in table}
    out = []
    for ch in text.upper():
        if ch in table:
            opts = table[ch]
            out.append(opts[counters[ch] % len(opts)])
            counters[ch] += 1
    return " ".join(out)


def decrypt(code: str) -> str:
    rev = {s: ch for ch, syms in build_table().items() for s in syms}
    return "".join(rev[s] for s in code.split())


if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) or "Meet me at ten"
    enc = encrypt(msg)
    print(enc)
    assert decrypt(enc) == "".join(c for c in msg.upper() if c.isalpha())
