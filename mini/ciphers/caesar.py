"""Caesar cipher with brute force: python caesar.py enc 3 "hello" | dec 3 "khoor" | crack "khoor zruog" """
import sys, string


def shift(text: str, k: int) -> str:
    out = []
    for ch in text:
        if ch in string.ascii_lowercase:
            out.append(chr((ord(ch) - 97 + k) % 26 + 97))
        elif ch in string.ascii_uppercase:
            out.append(chr((ord(ch) - 65 + k) % 26 + 65))
        else:
            out.append(ch)
    return "".join(out)


def score(text: str) -> float:
    """Higher = more English-like (letter frequency weights)."""
    w = dict(zip("etaoinshrdlu", range(12, 0, -1)))
    return sum(w.get(c, 0) for c in text.lower())


def crack(text: str) -> tuple[int, str]:
    return max(((k, shift(text, -k)) for k in range(26)), key=lambda t: score(t[1]))


if __name__ == "__main__":
    a = sys.argv[1:] or ["crack", "Khoor Zruog, wklv lv ixq"]
    if a[0] == "enc":
        print(shift(a[2], int(a[1])))
    elif a[0] == "dec":
        print(shift(a[2], -int(a[1])))
    else:
        k, t = crack(a[1])
        print(f"key {k}: {t}")
