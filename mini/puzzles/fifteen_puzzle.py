"""15-puzzle: shuffle a board, then solve it optimally with IDA* + Manhattan + linear conflict.

Run: python fifteen_puzzle.py [shuffle_moves] [seed]   (default 40 moves)
"""
from __future__ import annotations

import random
import sys

N = 4
GOAL = tuple(list(range(1, N * N)) + [0])
MOVES = {"U": -N, "D": N, "L": -1, "R": 1}


def neighbors(board: tuple[int, ...]):
    z = board.index(0)
    r, c = divmod(z, N)
    for name, d in MOVES.items():
        if (name == "U" and r == 0) or (name == "D" and r == N - 1) or \
           (name == "L" and c == 0) or (name == "R" and c == N - 1):
            continue
        b = list(board)
        b[z], b[z + d] = b[z + d], b[z]
        yield name, tuple(b)


def heuristic(board: tuple[int, ...]) -> int:
    h = 0
    for i, v in enumerate(board):
        if v:
            gr, gc = divmod(v - 1, N)
            r, c = divmod(i, N)
            h += abs(gr - r) + abs(gc - c)
    # linear conflicts in rows and columns
    for line in range(N):
        row = [board[line * N + c] for c in range(N)]
        rv = [v for v in row if v and (v - 1) // N == line]
        h += 2 * sum(1 for a in range(len(rv)) for b in range(a + 1, len(rv)) if rv[a] > rv[b])
        col = [board[r * N + line] for r in range(N)]
        cv = [v for v in col if v and (v - 1) % N == line]
        h += 2 * sum(1 for a in range(len(cv)) for b in range(a + 1, len(cv)) if cv[a] > cv[b])
    return h


def solve(start: tuple[int, ...]) -> list[str]:
    """Return an optimal list of blank moves taking ``start`` to GOAL."""
    path: list[str] = []
    seen = {start}

    def search(board, g, bound):
        f = g + heuristic(board)
        if f > bound:
            return f
        if board == GOAL:
            return True
        best = float("inf")
        for name, nb in neighbors(board):
            if nb in seen:
                continue
            seen.add(nb)
            path.append(name)
            t = search(nb, g + 1, bound)
            if t is True:
                return True
            best = min(best, t)
            path.pop()
            seen.discard(nb)
        return best

    bound = heuristic(start)
    while True:
        t = search(start, 0, bound)
        if t is True:
            return path
        bound = t


def shuffle(moves: int, rng: random.Random) -> tuple[int, ...]:
    board = GOAL
    for _ in range(moves):
        board = rng.choice(list(neighbors(board)))[1]
    return board


def show(board: tuple[int, ...]) -> str:
    return "\n".join(" ".join(f"{v:2}" if v else " ." for v in board[r * N:(r + 1) * N]) for r in range(N))


if __name__ == "__main__":
    moves = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
    board = shuffle(moves, random.Random(seed))
    print(show(board), "\n")
    sol = solve(board)
    print(f"Optimal solution: {len(sol)} moves")
    print(" ".join(sol))
