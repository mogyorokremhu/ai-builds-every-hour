"""Rule 184 traffic model: cars (1) move right when the cell ahead is free."""
import random
import sys


def step(cells):
    n = len(cells)
    return [
        1 if (cells[i] == 0 and cells[i - 1] == 1) or (cells[i] == 1 and cells[(i + 1) % n] == 1) else 0
        for i in range(n)
    ]


def flow(cells):
    """Fraction of cars that can move this step."""
    n = len(cells)
    cars = sum(cells)
    moving = sum(1 for i in range(n) if cells[i] and not cells[(i + 1) % n])
    return moving / cars if cars else 0.0


if __name__ == "__main__":
    density = float(sys.argv[1]) if len(sys.argv) > 1 else 0.35
    random.seed(5)
    c = [int(random.random() < density) for _ in range(64)]
    for t in range(24):
        print("".join("#" if x else "." for x in c), f"flow={flow(c):.2f}")
        c = step(c)
