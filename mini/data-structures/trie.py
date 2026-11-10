"""Prefix tree (trie) with autocomplete. Usage: python trie.py [prefix]"""
import sys


class Trie:
    def __init__(self) -> None:
        self.root: dict = {}

    def add(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def _find(self, prefix: str):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def __contains__(self, word: str) -> bool:
        n = self._find(word)
        return bool(n and "$" in n)

    def complete(self, prefix: str) -> list:
        """All stored words starting with prefix, sorted."""
        n = self._find(prefix)
        out: list = []

        def walk(node, acc):
            for k in sorted(node):
                if k == "$":
                    out.append(acc)
                else:
                    walk(node[k], acc + k)

        if n is not None:
            walk(n, prefix)
        return out


if __name__ == "__main__":
    t = Trie()
    for w in "car card care careful cart cat dog dot dove".split():
        t.add(w)
    p = sys.argv[1] if len(sys.argv) > 1 else "car"
    print(f"{p!r} ->", t.complete(p))
    print("'cat' in trie:", "cat" in t, "| 'ca' in trie:", "ca" in t)
