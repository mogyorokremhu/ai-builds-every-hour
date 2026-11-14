"""2048 on a 4x4 board. `--auto` plays greedy moves (most empty cells) and prints the final board."""
import random
import sys


def slide_row(row: list[int]) -> list[int]:
    tiles = [v for v in row if v]
    out: list[int] = []
    i = 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            out.append(tiles[i] * 2)
            i += 2
        else:
            out.append(tiles[i])
            i += 1
    return out + [0] * (4 - len(out))


def move(board: list[list[int]], d: str) -> list[list[int]]:
    if d in "ud":
        cols = [list(c) for c in zip(*board)]
        cols = [slide_row(c if d == "u" else c[::-1]) for c in cols]
        cols = [c if d == "u" else c[::-1] for c in cols]
        return [list(r) for r in zip(*cols)]
    return [slide_row(r if d == "l" else r[::-1]) if d == "l" else slide_row(r[::-1])[::-1] for r in board]


def spawn(board: list[list[int]]) -> None:
    empty = [(r, c) for r in range(4) for c in range(4) if not board[r][c]]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = 4 if random.random() < 0.1 else 2


def show(board: list[list[int]]) -> None:
    for row in board:
        print(" ".join(f"{v or '.':>4}" for v in row))


def main() -> None:
    board = [[0] * 4 for _ in range(4)]
    spawn(board)
    spawn(board)
    auto = "--auto" in sys.argv
    while True:
        options = [(d, move(board, d)) for d in "udlr"]
        options = [(d, b) for d, b in options if b != board]
        if not options:
            break
        if auto:
            d, board = max(options, key=lambda o: sum(v == 0 for r in o[1] for v in r))
        else:
            show(board)
            try:
                k = input("w/a/s/d> ").strip().lower()
            except EOFError:
                return
            m = {"w": "u", "s": "d", "a": "l", "d": "r"}.get(k)
            pick = [b for d, b in options if d == m]
            if not pick:
                continue
            board = pick[0]
        spawn(board)
    show(board)
    print("game over, max tile", max(max(r) for r in board))


if __name__ == "__main__":
    main()
