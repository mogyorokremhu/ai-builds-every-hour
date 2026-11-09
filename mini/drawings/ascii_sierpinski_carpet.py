"""Sierpinski carpet: python ascii_sierpinski_carpet.py [depth]"""
import sys

def carpet(n):
    size = 3 ** n
    rows = []
    for y in range(size):
        row = ""
        for x in range(size):
            a, b, hole = x, y, False
            while a or b:
                if a % 3 == 1 and b % 3 == 1:
                    hole = True
                    break
                a //= 3
                b //= 3
            row += "  " if hole else "██"
        rows.append(row)
    return "\n".join(rows)

if __name__ == "__main__":
    print(carpet(int(sys.argv[1]) if len(sys.argv) > 1 else 3))
