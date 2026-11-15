"""Break a Caesar cipher by letter-frequency chi-squared scoring. Usage: python frequency_attack.py "ciphertext" """
import sys

ENGLISH = [8.17, 1.49, 2.78, 4.25, 12.7, 2.23, 2.02, 6.09, 6.97, 0.15, 0.77, 4.03, 2.41,
           6.75, 7.51, 1.93, 0.1, 5.99, 6.33, 9.06, 2.76, 0.98, 2.36, 0.15, 1.97, 0.07]


def shift(s: str, n: int) -> str:
    return "".join(chr((ord(c.lower()) - 97 + n) % 26 + 97) if c.isascii() and c.isalpha() else c for c in s)


def chi2(s: str) -> float:
    letters = [c for c in s.lower() if c.isascii() and c.isalpha()]
    total = len(letters) or 1
    return sum((letters.count(chr(97 + i)) - total * ENGLISH[i] / 100) ** 2 / (total * ENGLISH[i] / 100)
               for i in range(26))


def crack(ct: str) -> tuple[int, str]:
    best = min(range(26), key=lambda k: chi2(shift(ct, -k)))
    return best, shift(ct, -best)


if __name__ == "__main__":
    ct = " ".join(sys.argv[1:]) or shift("the quick brown fox jumps over the lazy dog and runs away", 7)
    k, pt = crack(ct)
    print(f"key={k}: {pt}")
    assert chi2(pt) <= chi2(ct) or k == 0
