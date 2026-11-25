"""A tiny Bloom filter using double hashing over FNV-1a."""
import math
from fnv import fnv1a


class Bloom:
    def __init__(self, n_items: int, fp_rate: float = 0.01) -> None:
        self.m = max(8, int(-n_items * math.log(fp_rate) / (math.log(2) ** 2)))
        self.k = max(1, round(self.m / n_items * math.log(2)))
        self.bits = bytearray((self.m + 7) // 8)

    def _positions(self, item: str):
        data = item.encode()
        h1, h2 = fnv1a(data), fnv1a(data[::-1] + b"#") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def add(self, item: str) -> None:
        for p in self._positions(item):
            self.bits[p // 8] |= 1 << (p % 8)

    def __contains__(self, item: str) -> bool:
        return all(self.bits[p // 8] >> (p % 8) & 1 for p in self._positions(item))


if __name__ == "__main__":
    bf = Bloom(1000, 0.01)
    for i in range(1000):
        bf.add(f"key{i}")
    assert all(f"key{i}" in bf for i in range(1000))
    fp = sum(f"other{i}" in bf for i in range(10000)) / 10000
    print(f"bits={bf.m} hashes={bf.k} false-positive rate={fp:.3%}")
    assert fp < 0.03
