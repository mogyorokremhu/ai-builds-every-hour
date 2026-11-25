"""Vowel/consonant ratio and per-letter frequency histogram."""
from collections import Counter


def stats(text: str) -> dict:
    letters = [c for c in text.lower() if c.isalpha()]
    vowels = sum(c in "aeiou" for c in letters)
    return {"letters": len(letters), "vowels": vowels,
            "consonants": len(letters) - vowels,
            "ratio": vowels / max(1, len(letters) - vowels)}


def histogram(text: str) -> str:
    cnt = Counter(c for c in text.lower() if c.isalpha())
    return "\n".join(f"{c} {'#' * n}" for c, n in sorted(cnt.items()))


if __name__ == "__main__":
    s = stats("Hello World")
    assert s["letters"] == 10 and s["vowels"] == 3
    assert histogram("aab") == "a ##\nb #"
    print(s)
    print(histogram("the quick brown fox"))
    print("ok")
