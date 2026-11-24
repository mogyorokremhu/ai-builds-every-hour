"""Index of coincidence + Kasiski-style key-length guess for Vigenere text.
Usage: python railroad_check.py "ciphertext" (runs a self-test if no argument)"""
import sys
from collections import Counter


def ic(s: str) -> float:
    s = [c for c in s.upper() if c.isalpha()]
    n = len(s)
    if n < 2:
        return 0.0
    return sum(v * (v - 1) for v in Counter(s).values()) / (n * (n - 1))


def guess_key_length(s: str, maxlen: int = 12) -> int:
    s = "".join(c for c in s.upper() if c.isalpha())
    best, best_ic = 1, 0.0
    for L in range(1, maxlen + 1):
        avg = sum(ic(s[i::L]) for i in range(L)) / L
        if avg > best_ic + 0.005:
            best, best_ic = L, avg
    return best


if __name__ == "__main__":
    if len(sys.argv) > 1:
        t = " ".join(sys.argv[1:])
        print("IC:", round(ic(t), 4), "guessed key length:", guess_key_length(t))
    else:
        from vigenere import vig
        plain = ("the quick brown fox jumps over the lazy dog while the sun sets slowly behind "
                 "the distant hills and the evening wind carries the scent of pine across the valley ") * 4
        enc = vig(plain, "LEMON")
        print("plain IC", round(ic(plain), 4), "cipher IC", round(ic(enc), 4),
              "guess", guess_key_length(enc))
