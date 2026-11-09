"""Elementary cellular automaton triangle. python ascii_rule30.py [rule] [rows]"""
import sys


def main(rule: int = 30, rows: int = 32) -> None:
    w = rows * 2 + 1
    cells = [0] * w
    cells[w // 2] = 1
    for _ in range(rows):
        print("".join("#" if c else " " for c in cells).rstrip())
        cells = [(rule >> (cells[(i - 1) % w] * 4 + cells[i] * 2 + cells[(i + 1) % w])) & 1
                 for i in range(w)]


if __name__ == "__main__":
    a = sys.argv[1:]
    main(int(a[0]) if a else 30, int(a[1]) if len(a) > 1 else 32)
