"""Nim: take 1-3 sticks from a pile; whoever takes the last stick wins. `--auto` plays AI vs random."""
import random
import sys


def best_move(n: int) -> int:
    """Leave a multiple of 4 when possible."""
    m = n % 4
    return m if m else random.randint(1, min(3, n))


def main() -> None:
    n, turn = 21, 0  # turn 0 = you / AI-1, 1 = opponent
    auto = "--auto" in sys.argv
    while n > 0:
        if turn == 0 and not auto:
            try:
                take = int(input(f"{n} sticks, take 1-3> "))
            except (EOFError, ValueError):
                return
            if not 1 <= take <= min(3, n):
                continue
        elif turn == 0:
            take = best_move(n)
        else:
            take = best_move(n) if not auto else random.randint(1, min(3, n))
        n -= take
        print(f"player {turn} takes {take}, {n} left")
        if n == 0:
            print(f"player {turn} wins!")
        turn ^= 1


if __name__ == "__main__":
    main()
