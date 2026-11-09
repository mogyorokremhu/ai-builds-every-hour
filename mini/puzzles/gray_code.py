"""Gray code: generate, convert, and solve the Chinese-rings puzzle move order.  Usage: gray_code.py [bits]"""
import sys

def to_gray(n): return n ^ (n >> 1)

def from_gray(g):
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n

def rings_moves(bits):
    """Ring toggles (0-based) that take the Chinese rings from all-on to all-off: the bit changing between Gray codes."""
    seq = [to_gray(i) for i in range(2 ** bits)]
    return [(a ^ b).bit_length() - 1 for a, b in zip(seq, seq[1:])]

if __name__ == "__main__":
    b = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    for i in range(2 ** b):
        g = to_gray(i)
        assert from_gray(g) == i
        print(f"{i:3d} {g:0{b}b}")
    print("ring toggles:", rings_moves(b))
