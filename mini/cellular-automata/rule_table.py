"""Print every Wolfram elementary rule's behaviour as a small picture: python rule_table.py 30 90 110"""
import sys


def evolve(rule: int, width: int = 31, steps: int = 12):
    row = [0] * width
    row[width // 2] = 1
    rows = [row]
    for _ in range(steps - 1):
        row = [(rule >> (row[(i - 1) % width] * 4 + row[i] * 2 + row[(i + 1) % width])) & 1 for i in range(width)]
        rows.append(row)
    return rows


if __name__ == "__main__":
    rules = [int(a) for a in sys.argv[1:]] or [30, 90, 110, 184]
    for r in rules:
        print(f"Rule {r}")
        for row in evolve(r):
            print("".join("#" if c else "." for c in row))
        print()
