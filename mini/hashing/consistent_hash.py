"""Consistent hash ring with virtual nodes; shows how few keys move when a node is added."""
import bisect
from fnv import fnv1a


def _h(s: str) -> int:
    """FNV-1a followed by a 64-bit avalanche mix (FNV alone clusters similar keys)."""
    x = fnv1a(s.encode(), 64)
    x ^= x >> 33
    x = (x * 0xFF51AFD7ED558CCD) & 0xFFFFFFFFFFFFFFFF
    x ^= x >> 33
    x = (x * 0xC4CEB9FE1A85EC53) & 0xFFFFFFFFFFFFFFFF
    return x ^ (x >> 33)


class Ring:
    def __init__(self, nodes=(), vnodes: int = 100) -> None:
        self.vnodes, self.keys, self.map = vnodes, [], {}
        for n in nodes:
            self.add(n)

    def add(self, node: str) -> None:
        for i in range(self.vnodes):
            h = _h(f"{node}#{i}")
            bisect.insort(self.keys, h)
            self.map[h] = node

    def get(self, key: str) -> str:
        i = bisect.bisect(self.keys, _h(key)) % len(self.keys)
        return self.map[self.keys[i]]


if __name__ == "__main__":
    items = [f"item{i}" for i in range(5000)]
    ring = Ring(["a", "b", "c", "d"])
    before = {k: ring.get(k) for k in items}
    ring.add("e")
    moved = sum(before[k] != ring.get(k) for k in items)
    print(f"{moved}/{len(items)} keys moved ({moved/len(items):.1%}); ideal is ~20%")
    assert all(ring.get(k) == "e" for k in items if before[k] != ring.get(k))
    assert moved / len(items) < 0.35
