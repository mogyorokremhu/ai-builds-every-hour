"""Huffman coding: build a prefix code from symbol frequencies."""
import heapq
from collections import Counter


def build_codes(text: str) -> dict[str, str]:
    heap = [[w, i, [ch, ""]] for i, (ch, w) in enumerate(Counter(text).items())]
    heapq.heapify(heap)
    if len(heap) == 1:
        return {heap[0][2][0]: "0"}
    n = len(heap)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        for p in a[2:]:
            p[1] = "0" + p[1]
        for p in b[2:]:
            p[1] = "1" + p[1]
        heapq.heappush(heap, [a[0] + b[0], n, *a[2:], *b[2:]])
        n += 1
    return dict(heap[0][2:])


def encode(text: str, codes: dict[str, str]) -> str:
    return "".join(codes[c] for c in text)


def decode(bits: str, codes: dict[str, str]) -> str:
    rev, out, cur = {v: k for k, v in codes.items()}, [], ""
    for b in bits:
        cur += b
        if cur in rev:
            out.append(rev[cur])
            cur = ""
    return "".join(out)


if __name__ == "__main__":
    text = "abracadabra alakazam"
    codes = build_codes(text)
    for ch, code in sorted(codes.items(), key=lambda kv: (len(kv[1]), kv[0])):
        print(repr(ch), code)
    bits = encode(text, codes)
    assert decode(bits, codes) == text
    print(f"{len(text) * 8} bits -> {len(bits)} bits")
