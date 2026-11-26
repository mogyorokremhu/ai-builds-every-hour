"""Lexical diversity: type-token ratio, hapax legomena, and a moving-average TTR."""
import re


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())


def ttr(words: list[str]) -> float:
    return len(set(words)) / len(words) if words else 0.0


def hapax(words: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return sorted(w for w, c in counts.items() if c == 1)


def mattr(words: list[str], window: int = 5) -> float:
    if len(words) < window:
        return ttr(words)
    vals = [ttr(words[i:i + window]) for i in range(len(words) - window + 1)]
    return sum(vals) / len(vals)


if __name__ == "__main__":
    w = tokens("the cat and the dog and the bird sat on the mat")
    assert abs(ttr(w) - 8 / 12) < 1e-9
    assert hapax(w) == ["bird", "cat", "dog", "mat", "on", "sat"]
    print(f"tokens={len(w)} ttr={ttr(w):.3f} mattr={mattr(w):.3f}")
    print("hapax:", hapax(w))
