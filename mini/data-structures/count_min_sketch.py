"""Count-Min Sketch: approximate frequency counts in fixed memory. Usage: python count_min_sketch.py"""
import hashlib
import math
import random


class CountMinSketch:
    def __init__(self, epsilon=0.01, delta=0.01):
        self.width = math.ceil(math.e / epsilon)
        self.depth = math.ceil(math.log(1 / delta))
        self.table = [[0] * self.width for _ in range(self.depth)]

    def _cols(self, item):
        for row in range(self.depth):
            d = hashlib.blake2b(f"{row}:{item}".encode(), digest_size=8).digest()
            yield row, int.from_bytes(d, "big") % self.width

    def add(self, item, count=1):
        for r, c in self._cols(item):
            self.table[r][c] += count

    def estimate(self, item):
        """Never underestimates; overestimates by <= epsilon*N with prob >= 1-delta."""
        return min(self.table[r][c] for r, c in self._cols(item))


if __name__ == "__main__":
    random.seed(1)
    cms, truth = CountMinSketch(0.005, 0.01), {}
    words = [f"w{int(random.paretovariate(1.2))}" for _ in range(20000)]
    for w in words:
        cms.add(w)
        truth[w] = truth.get(w, 0) + 1
    print(f"table {cms.depth}x{cms.width}, N={len(words)}")
    for w, n in sorted(truth.items(), key=lambda kv: -kv[1])[:5]:
        print(f"{w:>5}: true={n:5d} estimate={cms.estimate(w)}")
    assert all(cms.estimate(w) >= n for w, n in truth.items())
