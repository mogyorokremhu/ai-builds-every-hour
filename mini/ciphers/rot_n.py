"""ROT-N: shift letters by any N, plus brute-force of all 26 shifts. Usage: python rot_n.py [-d|-b] N "text" """
import sys


def rot(s: str, n: int) -> str:
    out = []
    for c in s:
        if c.isascii() and c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            out.append(chr(base + (ord(c) - base + n) % 26))
        else:
            out.append(c)
    return "".join(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    mode = args.pop(0) if args and args[0] in ("-d", "-b") else ""
    n = int(args.pop(0)) if args and args[0].lstrip("-").isdigit() else 13
    text = " ".join(args) or "Hello, World"
    if mode == "-b":
        for k in range(26):
            print(f"{k:2d}: {rot(text, k)}")
    else:
        res = rot(text, -n if mode == "-d" else n)
        print(res)
        assert rot(res, n if mode == "-d" else -n) == text
