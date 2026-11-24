"""Tower of Hanoi: solves for N discs (default 4), drawing the pegs after each move."""
import sys


def hanoi(n, a, b, c, out):
    if n:
        hanoi(n - 1, a, c, b, out)
        out.append((a, c))
        hanoi(n - 1, b, a, c, out)


def draw(pegs, n):
    for row in range(n - 1, -1, -1):
        print("   ".join((("#" * (2 * p[row] - 1)) if row < len(p) else "|").center(2 * n) for p in pegs))
    print("-" * (6 * n + 6))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    pegs = [list(range(n, 0, -1)), [], []]
    moves = []
    hanoi(n, 0, 1, 2, moves)
    draw(pegs, n)
    for a, c in moves:
        pegs[c].append(pegs[a].pop())
        print(f"move {'ABC'[a]} -> {'ABC'[c]}")
        draw(pegs, n)
    print(f"done in {len(moves)} moves (2^{n}-1 = {2**n - 1})")


if __name__ == "__main__":
    main()
