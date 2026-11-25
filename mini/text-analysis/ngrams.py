"""Character and word n-gram counter."""
from collections import Counter


def char_ngrams(text: str, n: int) -> Counter:
    t = "".join(c for c in text.lower() if c.isalpha() or c == " ")
    return Counter(t[i:i + n] for i in range(len(t) - n + 1))


def word_ngrams(text: str, n: int) -> Counter:
    w = text.lower().split()
    return Counter(" ".join(w[i:i + n]) for i in range(len(w) - n + 1))


if __name__ == "__main__":
    s = "the cat and the hat and the bat"
    assert word_ngrams(s, 2)["the cat"] == 1
    assert word_ngrams(s, 1)["the"] == 3
    assert char_ngrams("aaa", 2)["aa"] == 2
    print("top bigrams:", word_ngrams(s, 2).most_common(3))
    print("top char trigrams:", char_ngrams(s, 3).most_common(3))
    print("ok")
