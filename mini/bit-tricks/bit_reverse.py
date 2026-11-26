"""Bit reversal: loop, lookup-free divide-and-conquer swaps, and bit-reversal permutation.

Usage: python bit_reverse.py [value] [width]
"""
import sys


def reverse_loop(x: int, width: int = 8) -> int:
    r = 0
    for _ in range(width):
        r = (r << 1) | (x & 1)
        x >>= 1
    return r


def reverse32(x: int) -> int:
    """Reverse a 32-bit word with five mask-and-swap steps."""
    x = ((x >> 1) & 0x55555555) | ((x & 0x55555555) << 1)
    x = ((x >> 2) & 0x33333333) | ((x & 0x33333333) << 2)
    x = ((x >> 4) & 0x0F0F0F0F) | ((x & 0x0F0F0F0F) << 4)
    x = ((x >> 8) & 0x00FF00FF) | ((x & 0x00FF00FF) << 8)
    return ((x >> 16) | (x << 16)) & 0xFFFFFFFF


def bit_reversal_permutation(n_bits: int) -> list[int]:
    return [reverse_loop(i, n_bits) for i in range(1 << n_bits)]


if __name__ == "__main__":
    v = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0b1011
    w = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    print(f"{v:0{w}b} -> {reverse_loop(v, w):0{w}b}")
    print(f"reverse32({v:#x}) = {reverse32(v):#010x}")
    assert reverse_loop(v, 32) == reverse32(v)
    print("FFT order (3 bits):", bit_reversal_permutation(3))
