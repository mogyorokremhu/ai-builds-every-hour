"""Hill cipher (2x2) over A-Z. Usage: python hill.py [-d] a b c d "text"  (key matrix [[a,b],[c,d]])"""
import sys
from math import gcd


def hill(text: str, key: tuple[int, int, int, int], decrypt: bool = False) -> str:
    a, b, c, d = key
    det = (a * d - b * c) % 26
    if gcd(det, 26) != 1:
        raise ValueError("key matrix is not invertible mod 26")
    if decrypt:
        inv = pow(det, -1, 26)
        a, b, c, d = (inv * d) % 26, (-inv * b) % 26, (-inv * c) % 26, (inv * a) % 26
    letters = [ord(ch) - 65 for ch in text.upper() if ch.isascii() and ch.isalpha()]
    if len(letters) % 2:
        letters.append(23)  # pad with X
    out = []
    for i in range(0, len(letters), 2):
        x, y = letters[i], letters[i + 1]
        out.append(chr(65 + (a * x + b * y) % 26))
        out.append(chr(65 + (c * x + d * y) % 26))
    return "".join(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    dec = bool(args and args[0] == "-d")
    if dec:
        args = args[1:]
    key = tuple(int(v) for v in args[:4]) if len(args) >= 4 else (3, 3, 2, 5)
    msg = " ".join(args[4:]) or "HELP"
    print(hill(msg, key, dec))
    assert hill(hill("HELPME", (3, 3, 2, 5)), (3, 3, 2, 5), True) == "HELPME"
    assert hill("HELP", (3, 3, 2, 5)) == "HIAT"
