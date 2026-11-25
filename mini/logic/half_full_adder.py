"""Ripple-carry adder built from gate-level half/full adders."""


def half_adder(a: int, b: int) -> tuple[int, int]:
    return a ^ b, a & b


def full_adder(a: int, b: int, c: int) -> tuple[int, int]:
    s1, c1 = half_adder(a, b)
    s2, c2 = half_adder(s1, c)
    return s2, c1 | c2


def add(x: int, y: int, bits: int = 8) -> int:
    carry, out = 0, 0
    for i in range(bits):
        s, carry = full_adder((x >> i) & 1, (y >> i) & 1, carry)
        out |= s << i
    return out | (carry << bits)


if __name__ == "__main__":
    for x, y in [(0, 0), (13, 29), (255, 255), (100, 155)]:
        r = add(x, y)
        print(f"{x} + {y} = {r}")
        assert r == x + y
    print("ok")
