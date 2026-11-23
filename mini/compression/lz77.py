"""LZ77: emit (offset, length, next_char) triples referencing a sliding window."""


def encode(s: str, window: int = 255) -> list[tuple[int, int, str]]:
    out, i = [], 0
    while i < len(s):
        best_off = best_len = 0
        for j in range(max(0, i - window), i):
            k = 0
            while i + k < len(s) - 1 and s[j + k] == s[i + k]:
                k += 1
            if k > best_len:
                best_off, best_len = i - j, k
        out.append((best_off, best_len, s[i + best_len]))
        i += best_len + 1
    return out


def decode(triples: list[tuple[int, int, str]]) -> str:
    out: list[str] = []
    for off, ln, ch in triples:
        for _ in range(ln):
            out.append(out[-off])
        out.append(ch)
    return "".join(out)


if __name__ == "__main__":
    text = "abracadabra abracadabra"
    enc = encode(text)
    print(enc)
    assert decode(enc) == text
    print("round trip ok")
