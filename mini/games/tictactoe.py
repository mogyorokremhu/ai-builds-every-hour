"""Tic-tac-toe vs an unbeatable minimax AI. `--auto` runs AI vs AI (always a draw)."""
import sys

LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]


def winner(b):
    for a, c, d in LINES:
        if b[a] != " " and b[a] == b[c] == b[d]:
            return b[a]
    return None


def minimax(b, me, turn):
    """Return (score, move) from `me`'s view: +1 win, 0 draw, -1 loss."""
    w = winner(b)
    if w:
        return (1 if w == me else -1), None
    moves = [i for i, c in enumerate(b) if c == " "]
    if not moves:
        return 0, None
    best = None
    for m in moves:
        b[m] = turn
        s, _ = minimax(b, me, "O" if turn == "X" else "X")
        b[m] = " "
        if best is None or (s > best[0] if turn == me else s < best[0]):
            best = (s, m)
    return best


def show(b):
    print("\n-+-+-\n".join("|".join(b[r*3:r*3+3]) for r in range(3)) + "\n")


def main() -> None:
    b, turn, auto = [" "] * 9, "X", "--auto" in sys.argv
    while not winner(b) and " " in b:
        if turn == "X" and not auto:
            try:
                m = int(input("your move 0-8> "))
            except (EOFError, ValueError):
                return
            if not 0 <= m <= 8 or b[m] != " ":
                continue
        else:
            m = minimax(b, turn, turn)[1]
        b[m] = turn
        show(b)
        turn = "O" if turn == "X" else "X"
    print(f"{winner(b)} wins!" if winner(b) else "Draw.")


if __name__ == "__main__":
    main()
