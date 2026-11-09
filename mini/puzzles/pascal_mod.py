"""Pascal's triangle mod m, drawn as ASCII (Sierpinski for m=2).  Usage: pascal_mod.py [rows] [mod]"""
import sys

def rows(n, m):
    row = [1 % m]
    for _ in range(n):
        yield row
        row = [1 % m] + [(a + b) % m for a, b in zip(row, row[1:])] + [1 % m]

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    glyphs = " .:*#%@oxO"
    for i, r in enumerate(rows(n, m)):
        print(" " * (n - i) + " ".join(glyphs[v % len(glyphs)] if v else " " for v in r))

if __name__ == "__main__":
    main()
