"""Julia sets in ASCII: pass a complex constant, or get a tour of famous ones.

    python ascii_julia.py              # four classic constants
    python ascii_julia.py -0.8 0.156   # your own c = re + im*i
"""
import sys

CHARS = " .,:;-=+*#%@"
W, H, ITER = 76, 26, 80
CLASSICS = ((-0.8, 0.156), (0.285, 0.01), (-0.4, 0.6), (-0.70176, -0.3842))


def julia(c: complex, w: int = W, h: int = H, iters: int = ITER) -> list[str]:
    rows = []
    for row in range(h):
        line = []
        for col in range(w):
            z = complex(-1.7 + col * 3.4 / w, -1.1 + row * 2.2 / h)
            n = 0
            while abs(z) <= 2 and n < iters:
                z = z * z + c
                n += 1
            line.append(CHARS[(n * (len(CHARS) - 1)) // iters])
        rows.append("".join(line))
    return rows


def main(argv: list[str]) -> None:
    consts = [(float(argv[0]), float(argv[1]))] if len(argv) >= 2 else CLASSICS
    for re, im in consts:
        print(f"c = {re} {'+' if im >= 0 else '-'} {abs(im)}i")
        print("\n".join(julia(complex(re, im))))
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
