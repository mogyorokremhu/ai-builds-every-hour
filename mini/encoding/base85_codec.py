"""Hand-written Ascii85 (base85) encoder/decoder, checked against the stdlib."""
import base64


def encode(data: bytes) -> str:
    out = []
    for i in range(0, len(data), 4):
        chunk = data[i:i + 4]
        pad = 4 - len(chunk)
        n = int.from_bytes(chunk + b"\0" * pad, "big")
        if n == 0 and pad == 0:
            out.append("z")
            continue
        digits = []
        for _ in range(5):
            n, r = divmod(n, 85)
            digits.append(chr(r + 33))
        out.append("".join(reversed(digits))[:5 - pad])
    return "".join(out)


def decode(text: str) -> bytes:
    out = bytearray()
    buf = []
    for c in text.replace("z", "!!!!!"):
        buf.append(ord(c) - 33)
        if len(buf) == 5:
            n = 0
            for d in buf:
                n = n * 85 + d
            out += n.to_bytes(4, "big")
            buf = []
    if buf:
        pad = 5 - len(buf)
        n = 0
        for d in buf + [84] * pad:
            n = n * 85 + d
        out += n.to_bytes(4, "big")[:4 - pad]
    return bytes(out)


if __name__ == "__main__":
    for s in (b"", b"a", b"Man is distinguished", b"\0\0\0\0hello", bytes(range(50))):
        e = encode(s)
        assert decode(e) == s, s
        assert e == base64.a85encode(s).decode(), (s, e)
        print(s[:20], "->", e[:40])
    print("ok")
