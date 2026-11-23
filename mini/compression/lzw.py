"""LZW compression with a growing dictionary of byte strings."""


def compress(data: str) -> list[int]:
    table = {chr(i): i for i in range(256)}
    w, out = "", []
    for c in data:
        if w + c in table:
            w += c
        else:
            out.append(table[w])
            table[w + c] = len(table)
            w = c
    if w:
        out.append(table[w])
    return out


def decompress(codes: list[int]) -> str:
    table = {i: chr(i) for i in range(256)}
    w = table[codes[0]]
    out = [w]
    for k in codes[1:]:
        entry = table[k] if k in table else w + w[0]
        out.append(entry)
        table[len(table)] = w + entry[0]
        w = entry
    return "".join(out)


if __name__ == "__main__":
    text = "TOBEORNOTTOBEORTOBEORNOT"
    codes = compress(text)
    print(codes)
    assert decompress(codes) == text
    print(f"{len(text)} chars -> {len(codes)} codes")
