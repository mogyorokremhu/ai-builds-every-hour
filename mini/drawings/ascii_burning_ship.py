"""Burning Ship fractal in shaded ASCII.  python ascii_burning_ship.py [max_iter]"""
import sys

def main(max_iter=40, w=72, h=26):
    shades = " .:-=+*#%@"
    for j in range(h):
        row = ""
        for i in range(w):
            c = complex(-2.2 + 3.0 * i / w, -2.0 + 2.4 * j / h)
            z, n = 0j, 0
            while abs(z) <= 2 and n < max_iter:
                z = complex(abs(z.real), abs(z.imag)) ** 2 + c
                n += 1
            row += "@" if n == max_iter else shades[n * (len(shades) - 1) // max_iter]
        print(row)

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
