"""Move-to-front transform: turns locally repeated symbols into small integers."""


def mtf_encode(data: str, alphabet: str | None = None) -> list[int]:
    table = list(alphabet if alphabet is not None else sorted(set(data)))
    out = []
    for ch in data:
        i = table.index(ch)
        out.append(i)
        table.insert(0, table.pop(i))
    return out


def mtf_decode(codes: list[int], alphabet: str) -> str:
    table = list(alphabet)
    out = []
    for i in codes:
        ch = table.pop(i)
        out.append(ch)
        table.insert(0, ch)
    return "".join(out)


if __name__ == "__main__":
    text = "aaabbbcccaaa"
    alpha = "".join(sorted(set(text)))
    codes = mtf_encode(text, alpha)
    print(text, "->", codes)
    assert mtf_decode(codes, alpha) == text
    print("round trip OK")
