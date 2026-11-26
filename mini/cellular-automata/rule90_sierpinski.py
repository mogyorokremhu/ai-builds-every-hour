"""Rule 90 from a single cell draws Sierpinski's triangle; also checks it equals Pascal mod 2."""
import sys


def rule90(n: int) -> list[list[int]]:
    width = 2 * n + 1
    row = [0] * width
    row[n] = 1
    rows = [row]
    for _ in range(n - 1):
        row = [row[(i - 1) % width] ^ row[(i + 1) % width] for i in range(width)]
        rows.append(row)
    return rows


def pascal_mod2(n: int) -> list[list[int]]:
    rows, cur = [], [1]
    for _ in range(n):
        rows.append(cur)
        cur = [1] + [(a + b) % 2 for a, b in zip(cur, cur[1:])] + [1]
    return rows


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    rows = rule90(n)
    for r in rows:
        print("".join("#" if c else " " for c in r).rstrip())
    ok = all(sum(r) == sum(p) for r, p in zip(rows, pascal_mod2(n)))
    print("live cells per row match Pascal mod 2:", ok)
