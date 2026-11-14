"""Lights Out on a 5x5 grid. `--auto` scrambles with random presses and solves by Gaussian elimination over GF(2)."""
import random
import sys

N = 5


def press(grid: list[int], r: int, c: int) -> None:
    for dr, dc in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < N and 0 <= cc < N:
            grid[rr * N + cc] ^= 1


def solve(grid: list[int]) -> list[int] | None:
    """Return press vector (0/1 per cell) that turns all lights off, or None."""
    n = N * N
    rows = []
    for i in range(n):
        row = [0] * (n + 1)
        r, c = divmod(i, N)
        for dr, dc in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            rr, cc = r + dr, c + dc
            if 0 <= rr < N and 0 <= cc < N:
                row[rr * N + cc] = 1
        row[n] = grid[i]
        rows.append(row)
    piv = []
    rank = 0
    for col in range(n):
        p = next((i for i in range(rank, n) if rows[i][col]), None)
        if p is None:
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        for i in range(n):
            if i != rank and rows[i][col]:
                rows[i] = [a ^ b for a, b in zip(rows[i], rows[rank])]
        piv.append(col)
        rank += 1
    if any(r[n] for r in rows[rank:]):
        return None
    sol = [0] * n
    for i, col in enumerate(piv):
        sol[col] = rows[i][n]
    return sol


def show(grid: list[int]) -> None:
    print("  " + " ".join(str(i + 1) for i in range(N)))
    for r in range(N):
        print(chr(65 + r) + " " + " ".join("#" if grid[r * N + c] else "." for c in range(N)))


def main() -> None:
    grid = [0] * (N * N)
    for _ in range(12):
        press(grid, random.randrange(N), random.randrange(N))
    show(grid)
    if "--auto" in sys.argv:
        sol = solve(grid)
        moves = [i for i, v in enumerate(sol or []) if v]
        for i in moves:
            press(grid, *divmod(i, N))
        print(f"solved with {len(moves)} presses")
        show(grid)
        return
    while any(grid):
        try:
            cmd = input("press (e.g. B3)> ").strip().upper()
        except EOFError:
            return
        if len(cmd) == 2 and cmd[0] in "ABCDE" and cmd[1] in "12345":
            press(grid, ord(cmd[0]) - 65, int(cmd[1]) - 1)
            show(grid)
    print("all lights out!")


if __name__ == "__main__":
    main()
