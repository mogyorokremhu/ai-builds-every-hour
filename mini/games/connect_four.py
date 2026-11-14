"""Connect Four vs a depth-4 minimax AI. `--auto` pits the AI against a random player."""
import random
import sys

ROWS, COLS = 6, 7


def drop(board, col, p):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ".":
            board[r][col] = p
            return r
    return None


def wins(board, p):
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                if all(0 <= r + dr * i < ROWS and 0 <= c + dc * i < COLS
                       and board[r + dr * i][c + dc * i] == p for i in range(4)):
                    return True
    return False


def valid(board):
    return [c for c in range(COLS) if board[0][c] == "."]


def minimax(board, depth, alpha, beta, me, turn):
    other = "O" if me == "X" else "X"
    if wins(board, me):
        return 1000 + depth
    if wins(board, other):
        return -1000 - depth
    moves = valid(board)
    if depth == 0 or not moves:
        return sum(3 for r in range(ROWS) if board[r][3] == me) - sum(3 for r in range(ROWS) if board[r][3] == other)
    best = -10**9 if turn == me else 10**9
    for c in moves:
        r = drop(board, c, turn)
        v = minimax(board, depth - 1, alpha, beta, me, other if turn == me else me)
        board[r][c] = "."
        if turn == me:
            best = max(best, v)
            alpha = max(alpha, v)
        else:
            best = min(best, v)
            beta = min(beta, v)
        if alpha >= beta:
            break
    return best


def ai_move(board, p):
    other = "O" if p == "X" else "X"
    scored = []
    for c in valid(board):
        r = drop(board, c, p)
        scored.append((minimax(board, 3, -10**9, 10**9, p, other), -abs(c - 3), c))
        board[r][c] = "."
    return max(scored)[2]


def show(board):
    print("\n".join(" ".join(row) for row in board))
    print("0 1 2 3 4 5 6\n")


def main() -> None:
    auto = "--auto" in sys.argv
    board = [["."] * COLS for _ in range(ROWS)]
    turn = "X"
    while valid(board):
        if turn == "X":
            col = ai_move(board, "X") if auto else None
            if col is None:
                try:
                    col = int(input("column 0-6> "))
                except (EOFError, ValueError):
                    return
                if col not in valid(board):
                    continue
        else:
            col = random.choice(valid(board)) if auto else ai_move(board, "O")
        drop(board, col, turn)
        if wins(board, turn):
            show(board)
            print(f"{turn} wins!")
            return
        turn = "O" if turn == "X" else "X"
    show(board)
    print("draw")


if __name__ == "__main__":
    main()
