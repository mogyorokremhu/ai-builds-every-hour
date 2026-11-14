"""Skip list: probabilistic sorted set. Usage: python skip_list.py"""
import random


class _Node:
    def __init__(self, key, level: int) -> None:
        self.key = key
        self.next = [None] * level


class SkipList:
    MAX = 16

    def __init__(self, p: float = 0.5, seed: int = 1) -> None:
        self.head = _Node(None, self.MAX)
        self.level = 1
        self.p = p
        self.rng = random.Random(seed)
        self.size = 0

    def _random_level(self) -> int:
        lvl = 1
        while lvl < self.MAX and self.rng.random() < self.p:
            lvl += 1
        return lvl

    def _find(self, key):
        update = [self.head] * self.MAX
        node = self.head
        for i in range(self.level - 1, -1, -1):
            while node.next[i] and node.next[i].key < key:
                node = node.next[i]
            update[i] = node
        return update, node.next[0]

    def add(self, key) -> bool:
        update, nxt = self._find(key)
        if nxt and nxt.key == key:
            return False
        lvl = self._random_level()
        self.level = max(self.level, lvl)
        node = _Node(key, lvl)
        for i in range(lvl):
            node.next[i] = update[i].next[i]
            update[i].next[i] = node
        self.size += 1
        return True

    def __contains__(self, key) -> bool:
        _, nxt = self._find(key)
        return bool(nxt and nxt.key == key)

    def remove(self, key) -> bool:
        update, nxt = self._find(key)
        if not nxt or nxt.key != key:
            return False
        for i in range(len(nxt.next)):
            update[i].next[i] = nxt.next[i]
        self.size -= 1
        return True

    def __iter__(self):
        node = self.head.next[0]
        while node:
            yield node.key
            node = node.next[0]

    def __len__(self) -> int:
        return self.size


if __name__ == "__main__":
    s = SkipList()
    for k in random.Random(7).sample(range(100), 30):
        s.add(k)
    items = list(s)
    assert items == sorted(items) and len(s) == 30
    victim = items[5]
    assert victim in s and s.remove(victim) and victim not in s
    print(f"{len(s)} keys, {s.level} levels:", list(s)[:10], "...")
