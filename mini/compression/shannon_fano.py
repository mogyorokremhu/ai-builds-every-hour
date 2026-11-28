"""Shannon-Fano coding: recursively split sorted symbols into near-equal-weight halves."""
from collections import Counter


def build(freqs: list[tuple[str, int]], prefix: str = "") -> dict[str, str]:
    if len(freqs) == 1:
        return {freqs[0][0]: prefix or "0"}
    total, acc, best, cut = sum(f for _, f in freqs), 0, None, 1
    for i in range(1, len(freqs)):
        acc += freqs[i - 1][1]
        diff = abs(total - 2 * acc)
        if best is None or diff < best:
            best, cut = diff, i
    codes = build(freqs[:cut], prefix + "0")
    codes.update(build(freqs[cut:], prefix + "1"))
    return codes


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
    text = "this is an example of shannon fano coding"
    freqs = sorted(Counter(text).items(), key=lambda kv: (-kv[1], kv[0]))
    codes = build(freqs)
    for sym, code in sorted(codes.items(), key=lambda kv: (len(kv[1]), kv[0])):
        print(repr(sym), code)
    bits = encode(text, codes)
    assert decode(bits, codes) == text
    print(f"{len(text) * 8} bits -> {len(bits)} bits")
