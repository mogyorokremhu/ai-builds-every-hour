"""1D totalistic cellular automaton (3-colour, code 0-2186 like Wolfram's k=3 r=1 codes)."""
import sys


def step(row: list, code: int) -> list:
    n = len(row)
    return [(code // 3 ** (row[i - 1] + row[i] + row[(i + 1) % n])) % 3 for i in range(n)]


if __name__ == "__main__":
    code = int(sys.argv[1]) if len(sys.argv) > 1 else 777
    width, gens = 61, 24
    row = [0] * width
    row[width // 2] = 1
    chars = " .#"
    print(f"code {code}")
    for _ in range(gens):
        print("".join(chars[c] for c in row))
        row = step(row, code)
