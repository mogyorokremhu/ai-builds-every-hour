"""Gray codes: encode/decode and a table (python gray_code.py [bits])."""
import sys


def to_gray(n: int) -> int:
    return n ^ (n >> 1)


def from_gray(g: int) -> int:
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n


def main(bits: int = 4) -> None:
    prev = None
    for i in range(1 << bits):
        g = to_gray(i)
        assert from_gray(g) == i
        if prev is not None:
            assert bin(prev ^ g).count("1") == 1  # one bit flips per step
        prev = g
        print(f"{i:>3}  {i:0{bits}b}  ->  {g:0{bits}b}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 4)
