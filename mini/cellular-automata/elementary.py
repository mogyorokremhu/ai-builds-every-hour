"""Wolfram elementary 1-D cellular automata: python elementary.py [rule] [rows]."""
import sys


def rule_step(row: list, rule: int) -> list:
    n = len(row)
    return [(rule >> (row[(i - 1) % n] * 4 + row[i] * 2 + row[(i + 1) % n])) & 1 for i in range(n)]


def run(rule: int = 90, rows: int = 16, width: int = 33) -> list:
    row = [0] * width
    row[width // 2] = 1
    out = []
    for _ in range(rows):
        out.append("".join("#" if c else " " for c in row).rstrip())
        row = rule_step(row, rule)
    return out


if __name__ == "__main__":
    rule = int(sys.argv[1]) if len(sys.argv) > 1 else 90
    rows = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    print(f"Rule {rule}")
    print("\n".join(run(rule, rows)))
