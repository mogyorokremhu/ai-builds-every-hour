"""LFU cache with O(1) get/put (frequency buckets). Usage: python lfu_cache.py"""
from collections import OrderedDict, defaultdict


class LFUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.vals: dict = {}
        self.freq: dict = {}
        self.buckets: dict[int, OrderedDict] = defaultdict(OrderedDict)
        self.min_freq = 0

    def _touch(self, key) -> None:
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq = f + 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key, default=None):
        if key not in self.vals:
            return default
        self._touch(key)
        return self.vals[key]

    def put(self, key, value) -> None:
        if self.cap <= 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) >= self.cap:
            old, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[old], self.freq[old]
        self.vals[key], self.freq[key] = value, 1
        self.buckets[1][key] = None
        self.min_freq = 1


if __name__ == "__main__":
    c = LFUCache(2)
    c.put("a", 1); c.put("b", 2)
    c.get("a")
    c.put("c", 3)  # evicts b (least frequent)
    print(c.get("b"), c.get("a"), c.get("c"))
    assert c.get("b") is None and c.get("a") == 1
