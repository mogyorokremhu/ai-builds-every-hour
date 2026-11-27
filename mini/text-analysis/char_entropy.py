"""Shannon entropy of characters and words in a text."""
import math
from collections import Counter


def entropy(items) -> float:
    """Shannon entropy in bits of a sequence of hashable items."""
    c = Counter(items)
    n = sum(c.values())
    return -sum(v / n * math.log2(v / n) for v in c.values()) if n else 0.0


if __name__ == "__main__":
    assert entropy("aaaa") == 0.0
    assert abs(entropy("abab") - 1.0) < 1e-9
    assert abs(entropy("abcd") - 2.0) < 1e-9
    text = "the quick brown fox jumps over the lazy dog"
    print("char entropy: %.3f bits" % entropy(text))
    print("word entropy: %.3f bits" % entropy(text.split()))
