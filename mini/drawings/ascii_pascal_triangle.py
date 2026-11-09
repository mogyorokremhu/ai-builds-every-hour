"""Pascal's triangle with odd entries marked (Sierpinski emerges): python ascii_pascal_triangle.py [rows]"""
import sys

def draw(n):
    row = [1]
    for i in range(n):
        print(" " * (n - i) + " ".join("#" if v % 2 else "." for v in row))
        row = [1] + [a + b for a, b in zip(row, row[1:])] + [1]

if __name__ == "__main__":
    draw(int(sys.argv[1]) if len(sys.argv) > 1 else 16)
