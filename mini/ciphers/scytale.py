"""Scytale transposition: text wrapped around a rod with N faces.

Usage: python scytale.py RODS "text" [-d]
"""
import sys


def encrypt(text: str, rods: int) -> str:
    """Write text in rows of `rods` letters and read down the columns."""
    pad = (-len(text)) % rods
    text += "_" * pad
    return "".join(text[i::rods] for i in range(rods))


def decrypt(cipher: str, rods: int) -> str:
    """Invert `encrypt` and strip the padding."""
    cols = len(cipher) // rods
    return "".join(cipher[i::cols] for i in range(cols)).rstrip("_")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "-d"]
    rods, text = int(args[0]), args[1]
    print(decrypt(text, rods) if "-d" in sys.argv else encrypt(text, rods))
