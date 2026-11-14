"""Minesweeper (9x9, 10 mines). `--auto` plays with simple deduction rules and guesses when stuck."""
import random
import sys

W = H = 9
MINES = 10


def neighbors(r: int, c: int):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if (dr or dc) and 0 <= r + dr < H and 0 <= c + dc < W:
                yield r + dr, c + dc


def main() -> None:
    cells = random.sample(range(W * H), MINES)
    mine = {divmod(i, W) for i in cells}
    count = {(r, c): sum(n in mine for n in neighbors(r, c)) for r in range(H) for c in range(W)}
    seen: set = set()
    flags: set = set()

    def reveal(r: int, c: int) -> bool:
        stack = [(r, c)]
        while stack:
            p = stack.pop()
            if p in seen or p in flags:
                continue
            if p in mine:
                return False
            seen.add(p)
            if count[p] == 0:
                stack.extend(neighbors(*p))
        return True

    reveal(*random.choice([p for p in count if p not in mine and count[p] == 0] or list(count)))
    alive = True
    while alive and len(seen) < W * H - MINES:
        progress = False
        for p in list(seen):
            hidden = [n for n in neighbors(*p) if n not in seen]
            unflagged = [n for n in hidden if n not in flags]
            if hidden and len(hidden) == count[p]:
                for n in unflagged:
                    flags.add(n)
                    progress = True
            elif unflagged and len([n for n in hidden if n in flags]) == count[p]:
                for n in unflagged:
                    alive = alive and reveal(*n)
                progress = True
        if not progress:
            guess = random.choice([p for p in count if p not in seen and p not in flags])
            alive = reveal(*guess)
    for r in range(H):
        print("".join("F" if (r, c) in flags else (str(count[r, c] or ".") if (r, c) in seen else "#") for c in range(W)))
    print("won!" if alive else "boom (hit a mine)")


if __name__ == "__main__":
    main()
