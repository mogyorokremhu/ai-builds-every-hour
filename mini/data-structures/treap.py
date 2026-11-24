"""Treap: a BST with random heap priorities (expected O(log n)). Usage: python treap.py"""
import random


class _N:
    __slots__ = ("key", "pri", "left", "right")

    def __init__(self, key, pri):
        self.key, self.pri, self.left, self.right = key, pri, None, None


def _split(t, key):
    """Split into (< key, >= key)."""
    if t is None:
        return None, None
    if t.key < key:
        a, b = _split(t.right, key)
        t.right = a
        return t, b
    a, b = _split(t.left, key)
    t.left = b
    return a, t


def _merge(a, b):
    if a is None or b is None:
        return a or b
    if a.pri > b.pri:
        a.right = _merge(a.right, b)
        return a
    b.left = _merge(a, b.left)
    return b


class Treap:
    def __init__(self, seed=None):
        self.root, self.rng, self.size = None, random.Random(seed), 0

    def __contains__(self, key):
        t = self.root
        while t:
            if key == t.key:
                return True
            t = t.left if key < t.key else t.right
        return False

    def insert(self, key):
        if key in self:
            return
        a, b = _split(self.root, key)
        self.root = _merge(_merge(a, _N(key, self.rng.random())), b)
        self.size += 1

    def delete(self, key):
        if key not in self:
            return
        a, b = _split(self.root, key)
        _, c = _split(b, key + 1 if isinstance(key, int) else key)
        self.root = _merge(a, c)
        self.size -= 1

    def __iter__(self):
        stack, t = [], self.root
        while stack or t:
            while t:
                stack.append(t)
                t = t.left
            t = stack.pop()
            yield t.key
            t = t.right

    def height(self):
        def h(t):
            return 0 if t is None else 1 + max(h(t.left), h(t.right))
        return h(self.root)


if __name__ == "__main__":
    t = Treap(seed=1)
    for i in range(1000):
        t.insert(i)  # sorted input, still balanced
    t.delete(500)
    print("size", t.size, "height", t.height(), "has 500:", 500 in t, "has 501:", 501 in t)
    assert list(t) == sorted(set(range(1000)) - {500})
