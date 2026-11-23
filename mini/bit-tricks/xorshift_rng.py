"""xorshift32 / xorshift64 pseudo-random generators with a bit-balance check."""


def xorshift32(seed: int):
    x = seed & 0xFFFFFFFF or 1
    while True:
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        yield x


def xorshift64(seed: int):
    x = seed & 0xFFFFFFFFFFFFFFFF or 1
    m = 0xFFFFFFFFFFFFFFFF
    while True:
        x ^= (x << 13) & m
        x ^= x >> 7
        x ^= (x << 17) & m
        yield x


if __name__ == "__main__":
    g = xorshift32(2463534242)
    first = [next(g) for _ in range(3)]
    assert first[0] == 723471715  # reference value for this seed
    print("xorshift32:", first)
    ones = sum(bin(next(g)).count("1") for _ in range(10000))
    print(f"mean set bits per 32-bit word: {ones / 10000:.2f} (ideal 16)")
    h = xorshift64(88172645463325252)
    print("xorshift64:", [next(h) for _ in range(2)])
