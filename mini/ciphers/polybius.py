"""Polybius square: each letter becomes a row/column digit pair (I/J share a cell).

Usage: python polybius.py "text" [-d]
"""
import sys

SQUARE = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def encrypt(text: str) -> str:
    out = []
    for ch in text.upper().replace("J", "I"):
        if ch in SQUARE:
            i = SQUARE.index(ch)
            out.append(f"{i // 5 + 1}{i % 5 + 1}")
        else:
            out.append(ch)
    return "".join(out)


def decrypt(code: str) -> str:
    out, i = [], 0
    while i < len(code):
        if code[i] in "12345" and i + 1 < len(code) and code[i + 1] in "12345":
            out.append(SQUARE[(int(code[i]) - 1) * 5 + int(code[i + 1]) - 1])
            i += 2
        else:
            out.append(code[i])
            i += 1
    return "".join(out)


if __name__ == "__main__":
    text = " ".join(a for a in sys.argv[1:] if a != "-d")
    print(decrypt(text) if "-d" in sys.argv else encrypt(text))
