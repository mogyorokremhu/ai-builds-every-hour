"""Golomb-Rice coding of non-negative integers (unary quotient + k-bit remainder)."""


def rice_encode(values: list[int], k: int) -> str:
    bits = []
    for v in values:
        q, r = v >> k, v & ((1 << k) - 1)
        bits.append("1" * q + "0" + (format(r, f"0{k}b") if k else ""))
    return "".join(bits)


def rice_decode(bits: str, k: int) -> list[int]:
    out, i = [], 0
    while i < len(bits):
        q = 0
        while bits[i] == "1":
            q += 1
            i += 1
        i += 1
        r = int(bits[i:i + k], 2) if k else 0
        i += k
        out.append((q << k) | r)
    return out


if __name__ == "__main__":
    data = [0, 1, 2, 7, 3, 12, 5, 0, 9]
    for k in (0, 1, 2, 3):
        enc = rice_encode(data, k)
        assert rice_decode(enc, k) == data
        print(f"k={k}: {len(enc)} bits")
    print("round trip OK")
