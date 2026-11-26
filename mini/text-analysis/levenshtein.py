"""Edit distance (Levenshtein) plus closest-word suggestion."""


def distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def suggest(word: str, vocab: list[str], n: int = 3) -> list[str]:
    return sorted(vocab, key=lambda v: (distance(word, v), v))[:n]


if __name__ == "__main__":
    assert distance("kitten", "sitting") == 3
    assert distance("", "abc") == 3
    assert distance("same", "same") == 0
    vocab = ["apple", "apply", "ample", "maple", "orange"]
    print(suggest("appel", vocab))
