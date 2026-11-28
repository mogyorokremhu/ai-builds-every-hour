"""Towers of Hanoi: recursive solver that prints moves and verifies the count 2**n - 1."""


def hanoi(n: int, src: str, dst: str, aux: str, moves: list[tuple[str, str]]) -> None:
    """Append the moves that shift n disks from src to dst."""
    if n == 0:
        return
    hanoi(n - 1, src, aux, dst, moves)
    moves.append((src, dst))
    hanoi(n - 1, aux, dst, src, moves)


if __name__ == "__main__":
    for n in (1, 2, 3, 4):
        moves: list[tuple[str, str]] = []
        hanoi(n, "A", "C", "B", moves)
        assert len(moves) == 2**n - 1
        print(f"{n} disks: {len(moves)} moves")
    moves = []
    hanoi(3, "A", "C", "B", moves)
    for i, (a, b) in enumerate(moves, 1):
        print(f"{i}. {a} -> {b}")
