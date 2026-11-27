"""4:1 multiplexer and 2:4 decoder from gates, with exhaustive checks."""
from itertools import product


def decoder(s1: int, s0: int) -> list[int]:
    return [(1 - s1) & (1 - s0), (1 - s1) & s0, s1 & (1 - s0), s1 & s0]


def mux4(d: list[int], s1: int, s0: int) -> int:
    out = 0
    for bit, sel in zip(d, decoder(s1, s0)):
        out |= bit & sel
    return out


if __name__ == "__main__":
    for s1, s0 in product((0, 1), repeat=2):
        assert decoder(s1, s0).index(1) == s1 * 2 + s0
        for d in product((0, 1), repeat=4):
            assert mux4(list(d), s1, s0) == d[s1 * 2 + s0]
    print("mux/decoder: ok")
