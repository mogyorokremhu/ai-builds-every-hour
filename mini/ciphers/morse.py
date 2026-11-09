"""Morse code encoder/decoder. Usage: python morse.py [-d] text..."""
import sys

CODE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.",
        "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.",
        "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-",
        "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..",
        "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
        "6": "-....", "7": "--...", "8": "---..", "9": "----."}
REV = {v: k for k, v in CODE.items()}


def encode(s: str) -> str:
    return " / ".join(" ".join(CODE[c] for c in w if c in CODE) for w in s.upper().split())


def decode(m: str) -> str:
    return " ".join("".join(REV.get(t, "?") for t in w.split()) for w in m.split("/"))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "-d":
        print(decode(" ".join(a[1:])))
    elif a:
        print(encode(" ".join(a)))
    else:
        m = encode("hello world 42")
        print(m)
        assert decode(m) == "HELLO WORLD 42"
