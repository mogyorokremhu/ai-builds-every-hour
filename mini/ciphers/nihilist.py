"""Nihilist cipher: Polybius square numbers added to a repeating keyword's numbers.
Usage: python nihilist.py [-d] square_key keyword "text" """
import sys


def square(key: str) -> dict[str, int]:
    seen = []
    for ch in (key.upper() + "ABCDEFGHIKLMNOPQRSTUVWXYZ").replace("J", "I"):
        if ch.isalpha() and ch not in seen:
            seen.append(ch)
    return {ch: (i // 5 + 1) * 10 + i % 5 + 1 for i, ch in enumerate(seen)}


def encrypt(text: str, skey: str, word: str) -> list[int]:
    sq = square(skey)
    t = [c for c in text.upper().replace("J", "I") if c in sq]
    w = [c for c in word.upper().replace("J", "I") if c in sq]
    return [sq[c] + sq[w[i % len(w)]] for i, c in enumerate(t)]


def decrypt(nums: list[int], skey: str, word: str) -> str:
    sq = square(skey)
    rev = {v: k for k, v in sq.items()}
    w = [c for c in word.upper().replace("J", "I") if c in sq]
    return "".join(rev[n - sq[w[i % len(w)]]] for i, n in enumerate(nums))


if __name__ == "__main__":
    args = sys.argv[1:]
    dec = bool(args and args[0] == "-d")
    if dec:
        args = args[1:]
    skey, word = (args[0], args[1]) if len(args) >= 2 else ("ZEBRA", "KEY")
    rest = args[2:]
    if dec:
        print(decrypt([int(x) for x in rest], skey, word))
    else:
        print(*encrypt(" ".join(rest) or "ATTACK", skey, word))
    assert decrypt(encrypt("HELLOWORLD", "ZEBRA", "KEY"), "ZEBRA", "KEY") == "HELLOWORLD"
