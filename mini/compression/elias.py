"""Elias gamma and delta universal codes for positive integers."""


def gamma(n: int) -> str:
    if n < 1:
        raise ValueError("n must be >= 1")
    b = bin(n)[2:]
    return "0" * (len(b) - 1) + b


def delta(n: int) -> str:
    if n < 1:
        raise ValueError("n must be >= 1")
    b = bin(n)[2:]
    return gamma(len(b)) + b[1:]


def decode_gamma(bits: str) -> list[int]:
    out, i = [], 0
    while i < len(bits):
        z = 0
        while bits[i] == "0":
            z += 1
            i += 1
        out.append(int(bits[i:i + z + 1], 2))
        i += z + 1
    return out


def decode_delta(bits: str) -> list[int]:
    out, i = [], 0
    while i < len(bits):
        z = 0
        while bits[i] == "0":
            z += 1
            i += 1
        length = int(bits[i:i + z + 1], 2)
        i += z + 1
        out.append(int("1" + bits[i:i + length - 1], 2) if length > 1 else 1)
        i += length - 1
    return out


if __name__ == "__main__":
    nums = [1, 2, 3, 10, 100, 1000]
    for n in nums:
        print(f"{n:5d}  gamma={gamma(n):<22} delta={delta(n)}")
    assert decode_gamma("".join(map(gamma, nums))) == nums
    assert decode_delta("".join(map(delta, nums))) == nums
    print("round trips ok")
