"""Printable 5x5 bingo cards (B-I-N-G-O column ranges, free centre).

Usage: python bingo.py [cards] [seed]
"""
import random
import sys


def card(rng: random.Random) -> list[list[str]]:
    """Return a 5x5 grid of strings; column c draws from 15c+1 .. 15c+15."""
    cols = [rng.sample(range(15 * c + 1, 15 * c + 16), 5) for c in range(5)]
    grid = [[str(cols[c][r]) for c in range(5)] for r in range(5)]
    grid[2][2] = "FREE"
    return grid


def render(grid: list[list[str]]) -> str:
    """Format a card as ASCII."""
    lines = ["  B     I     N     G     O  ", "+" + "-----+" * 5]
    for row in grid:
        lines.append("|" + "|".join(f"{v:^5}" for v in row) + "|")
        lines.append("+" + "-----+" * 5)
    return "\n".join(lines)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rng = random.Random(int(sys.argv[2])) if len(sys.argv) > 2 else random.Random()
    print("\n\n".join(render(card(rng)) for _ in range(n)))
