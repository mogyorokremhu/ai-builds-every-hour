"""Knight's tour on an NxN board using Warnsdorff's heuristic."""
import sys

MOVES = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]


def tour(n: int = 8, start: tuple[int, int] = (0, 0)):
    """Return an n x n grid of move numbers, or None if the heuristic fails."""
    board = [[0] * n for _ in range(n)]
    x, y = start
    board[y][x] = 1

    def onward(px: int, py: int):
        return [(px + dx, py + dy) for dx, dy in MOVES
                if 0 <= px + dx < n and 0 <= py + dy < n and board[py + dy][px + dx] == 0]

    for step in range(2, n * n + 1):
        cands = onward(x, y)
        if not cands:
            return None
        x, y = min(cands, key=lambda c: len(onward(*c)))
        board[y][x] = step
    return board


if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    b = tour(size)
    if b is None:
        print("no tour found")
    else:
        for row in b:
            print(" ".join(f"{v:3d}" for v in row))
