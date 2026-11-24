"""Flesch reading-ease score with a rough syllable counter."""
import re


def syllables(word: str) -> int:
    """Estimate syllables by counting vowel groups (minimum 1)."""
    w = word.lower()
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1 and not w.endswith("le"):
        n -= 1
    return max(n, 1)


def flesch(text: str) -> float:
    """Flesch reading ease: higher means easier."""
    sents = max(len(re.findall(r"[.!?]+", text)), 1)
    words = re.findall(r"[A-Za-z']+", text)
    syl = sum(syllables(w) for w in words)
    return 206.835 - 1.015 * len(words) / sents - 84.6 * syl / max(len(words), 1)


if __name__ == "__main__":
    easy = flesch("The cat sat on the mat. The dog ran.")
    hard = flesch("Notwithstanding considerable epistemological uncertainty, institutional implementation proceeded.")
    assert easy > hard
    print(f"easy={easy:.1f} hard={hard:.1f}")
