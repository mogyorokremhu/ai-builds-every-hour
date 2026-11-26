"""Classic uuencode: 3 bytes -> 4 printable chars, 45 bytes per line."""
import binascii


def _ch(v: int) -> str:
    return chr(v + 32) if v else "`"


def encode(data: bytes) -> str:
    lines = []
    for i in range(0, len(data), 45):
        chunk = data[i:i + 45]
        line = [_ch(len(chunk))]
        padded = chunk + b"\0" * (-len(chunk) % 3)
        for j in range(0, len(padded), 3):
            n = int.from_bytes(padded[j:j + 3], "big")
            line += [_ch((n >> s) & 63) for s in (18, 12, 6, 0)]
        lines.append("".join(line))
    lines.append("`")
    return "\n".join(lines)


def decode(text: str) -> bytes:
    out = bytearray()
    for line in text.splitlines():
        if not line or line == "`":
            continue
        length = (ord(line[0]) - 32) & 63
        vals = [(ord(c) - 32) & 63 for c in line[1:]]
        raw = bytearray()
        for j in range(0, len(vals), 4):
            a, b, c, d = (vals[j:j + 4] + [0, 0, 0, 0])[:4]
            n = (a << 18) | (b << 12) | (c << 6) | d
            raw += n.to_bytes(3, "big")
        out += raw[:length]
    return bytes(out)


if __name__ == "__main__":
    for s in (b"", b"cat", b"The quick brown fox jumps over the lazy dog" * 3):
        e = encode(s)
        assert decode(e) == s
        # cross-check each line against binascii
        for k in range(0, len(s), 45):
            assert e.splitlines()[k // 45] == binascii.b2a_uu(s[k:k + 45], backtick=True).decode().rstrip("\n")
    print(encode(b"Hello, uuencode!"))
    print("ok")
