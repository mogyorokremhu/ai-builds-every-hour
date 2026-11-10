"""Bloom filter: probabilistic set membership. Usage: python bloom_filter.py"""
import hashlib
import math


class Bloom:
    def __init__(self, n: int, fp_rate: float = 0.01) -> None:
        self.m = max(8, int(-n * math.log(fp_rate) / math.log(2) ** 2))
        self.k = max(1, round(self.m / n * math.log(2)))
        self.bits = bytearray(self.m // 8 + 1)

    def _hashes(self, item: str):
        for i in range(self.k):
            h = hashlib.sha256(f"{i}:{item}".encode()).digest()
            yield int.from_bytes(h[:8], "big") % self.m

    def add(self, item: str) -> None:
        for h in self._hashes(item):
            self.bits[h // 8] |= 1 << (h % 8)

    def __contains__(self, item: str) -> bool:
        return all(self.bits[h // 8] >> (h % 8) & 1 for h in self._hashes(item))


if __name__ == "__main__":
    b = Bloom(1000, 0.01)
    for i in range(1000):
        b.add(f"item{i}")
    assert all(f"item{i}" in b for i in range(1000))  # no false negatives
    fp = sum(f"other{i}" in b for i in range(10000))
    print(f"bits={b.m} hashes={b.k} false positives: {fp}/10000 ({fp/100:.2f}%)")
