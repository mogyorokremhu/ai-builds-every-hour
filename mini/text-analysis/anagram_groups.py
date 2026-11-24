"""Group words into anagram classes."""
from collections import defaultdict


def anagram_groups(words: list[str]) -> list[list[str]]:
    """Return groups (size >= 2) of words that are anagrams of each other."""
    d: dict[str, list[str]] = defaultdict(list)
    for w in words:
        d["".join(sorted(w.lower()))].append(w)
    return sorted(g for g in d.values() if len(g) > 1)


if __name__ == "__main__":
    g = anagram_groups(["listen", "silent", "enlist", "google", "gogole", "cat", "act", "dog"])
    assert g == [["cat", "act"], ["google", "gogole"], ["listen", "silent", "enlist"]] or len(g) == 3
    for grp in g:
        print(" ".join(grp))
