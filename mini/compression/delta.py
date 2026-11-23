"""Delta encoding: store differences between neighbours (great for slowly changing data)."""


def encode(xs: list[int]) -> list[int]:
    return [x - (xs[i - 1] if i else 0) for i, x in enumerate(xs)]


def decode(ds: list[int]) -> list[int]:
    out, acc = [], 0
    for d in ds:
        acc += d
        out.append(acc)
    return out


if __name__ == "__main__":
    data = [1000, 1002, 1003, 1003, 1007, 1006, 1010]
    enc = encode(data)
    print(enc)
    assert decode(enc) == data
    print("round trip ok")
