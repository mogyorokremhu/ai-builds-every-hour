"""Fantasy name generator from syllable tables. Usage: python names.py [count] [seed]"""
import random
import sys

START = ["Ar", "Bel", "Cor", "Dra", "El", "Fen", "Gal", "Hal", "Ith", "Kor", "Lum", "Mor", "Nar", "Or", "Syl", "Thal", "Val", "Zan"]
MID = ["a", "e", "i", "o", "an", "en", "ir", "or", "ad", "il", "ar", "eth"]
END = ["dor", "wen", "ric", "mir", "thas", "len", "ra", "dil", "gard", "ion", "bel", "rin", "us", "yn"]


def name(rng: random.Random) -> str:
    parts = [rng.choice(START)] + [rng.choice(MID) for _ in range(rng.choice((0, 1, 1)))] + [rng.choice(END)]
    return "".join(parts)


if __name__ == "__main__":
    a = sys.argv[1:]
    n = int(a[0]) if a else 10
    rng = random.Random(int(a[1])) if len(a) > 1 else random.Random()
    for _ in range(n):
        print(name(rng))
