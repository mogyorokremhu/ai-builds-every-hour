"""LZ78: dictionary of previously seen phrases, output (index, next_char) pairs."""


def lz78_encode(data: str) -> list[tuple[int, str]]:
    dic: dict[str, int] = {}
    out: list[tuple[int, str]] = []
    phrase = ""
    for ch in data:
        if phrase + ch in dic:
            phrase += ch
        else:
            out.append((dic.get(phrase, 0), ch))
            dic[phrase + ch] = len(dic) + 1
            phrase = ""
    if phrase:
        out.append((dic[phrase], ""))
    return out


def lz78_decode(pairs: list[tuple[int, str]]) -> str:
    entries = [""]
    out = []
    for idx, ch in pairs:
        s = entries[idx] + ch
        out.append(s)
        entries.append(s)
    return "".join(out)


if __name__ == "__main__":
    text = "abababababbabbab"
    enc = lz78_encode(text)
    print(enc)
    assert lz78_decode(enc) == text
    print("round trip OK")
