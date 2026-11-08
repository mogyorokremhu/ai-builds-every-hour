#!/usr/bin/env python3
"""Minesweeper with a logical auto-solver.

Play in the terminal, or watch the solver clear a board. The solver never guesses
while logic can progress: it applies the two basic rules (a number whose hidden
neighbours all must be mines / are all safe), then the *subset rule* on pairs of
constraints (if A's hidden cells ⊂ B's, then B − A holds B − A mines), and finally
exact enumeration of the frontier split into independent groups, which gives each
hidden cell a mine probability. Only when nothing is certain does it click the
cell with the lowest probability.

    python minesweeper.py                    # auto-solve a 16×16 board with 40 mines
    python minesweeper.py --games 200        # win rate of the solver over many boards
    python minesweeper.py --play --size 9 --mines 10
"""
from __future__ import annotations

import random
import sys
from itertools import combinations


class Board:
    def __init__(self, w: int, h: int, mines: int, rng: random.Random):
        self.w, self.h, self.n = w, h, mines
        self.rng = rng
        self.mines: set[tuple[int, int]] = set()
        self.open: set[tuple[int, int]] = set()
        self.flags: set[tuple[int, int]] = set()
        self.lost = False

    def cells(self):
        return [(x, y) for y in range(self.h) for x in range(self.w)]

    def around(self, c):
        x, y = c
        return [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                if (dx or dy) and 0 <= x + dx < self.w and 0 <= y + dy < self.h]

    def place(self, first):
        """Mines go anywhere except the first click and its neighbours (first click is a 0)."""
        safe = {first, *self.around(first)}
        pool = [c for c in self.cells() if c not in safe]
        self.mines = set(self.rng.sample(pool, self.n))

    def count(self, c) -> int:
        return sum(n in self.mines for n in self.around(c))

    def reveal(self, c) -> None:
        if not self.mines:
            self.place(c)
        if c in self.mines:
            self.lost = True
            return
        todo = [c]
        while todo:
            cur = todo.pop()
            if cur in self.open:
                continue
            self.open.add(cur)
            self.flags.discard(cur)
            if self.count(cur) == 0:
                todo.extend(n for n in self.around(cur) if n not in self.open)

    @property
    def won(self) -> bool:
        return not self.lost and len(self.open) == self.w * self.h - self.n

    def show(self, reveal_all: bool = False) -> str:
        rows = ["   " + "".join(f"{x % 10}" for x in range(self.w))]
        for y in range(self.h):
            row = ""
            for x in range(self.w):
                c = (x, y)
                if c in self.open:
                    k = self.count(c)
                    row += str(k) if k else " "
                elif reveal_all and c in self.mines:
                    row += "*"
                elif c in self.flags:
                    row += "F"
                else:
                    row += "·"
            rows.append(f"{y:2} {row}")
        return "\n".join(rows)


def constraints(b: Board):
    """(hidden unflagged cells, mines among them) for every open number on the frontier."""
    out = []
    for c in b.open:
        hidden = frozenset(n for n in b.around(c) if n not in b.open and n not in b.flags)
        if hidden:
            out.append((hidden, b.count(c) - sum(n in b.flags for n in b.around(c))))
    return out


def deduce(b: Board):
    """Certain (safe, mines) sets from the single and subset rules."""
    cons = list(set(constraints(b)))
    safe, mines = set(), set()
    for cells, k in cons:
        if k == 0:
            safe |= cells
        elif k == len(cells):
            mines |= cells
    if safe or mines:
        return safe, mines
    for (a, ka), (c, kc) in combinations(cons, 2):
        for (small, ks), (big, kb) in (((a, ka), (c, kc)), ((c, kc), (a, ka))):
            if small < big:
                rest, kr = big - small, kb - ks
                if kr == 0:
                    safe |= rest
                elif kr == len(rest):
                    mines |= rest
    return safe, mines


def probabilities(b: Board, max_group: int = 22):
    """Mine probability of each frontier cell by enumerating consistent assignments per group."""
    cons = list(set(constraints(b)))
    cells = sorted({c for cs, _ in cons for c in cs})
    # split the frontier into independent groups (cells linked through shared constraints)
    parent = {c: c for c in cells}

    def find(c):
        while parent[c] != c:
            parent[c] = parent[parent[c]]
            c = parent[c]
        return c

    for cs, _ in cons:
        first, *rest = list(cs)
        for o in rest:
            parent[find(o)] = find(first)
    groups: dict = {}
    for c in cells:
        groups.setdefault(find(c), []).append(c)
    prob = {}
    for group in groups.values():
        if len(group) > max_group:
            continue
        gset = set(group)
        gcons = [(cs, k) for cs, k in cons if cs <= gset]
        counts = {c: 0 for c in group}
        total = 0
        assign: dict = {}

        def ok_partial():
            for cs, k in gcons:
                known = [assign[c] for c in cs if c in assign]
                s = sum(known)
                if s > k or s + (len(cs) - len(known)) < k:
                    return False
            return True

        def rec(i):
            nonlocal total
            if i == len(group):
                total += 1
                for c in group:
                    counts[c] += assign[c]
                return
            for v in (0, 1):
                assign[group[i]] = v
                if ok_partial():
                    rec(i + 1)
                del assign[group[i]]

        rec(0)
        if total:
            for c in group:
                prob[c] = counts[c] / total
    return prob


def autoplay(b: Board, verbose: bool = False) -> bool:
    b.reveal((b.w // 2, b.h // 2))
    guesses = 0
    while not b.lost and not b.won:
        safe, mines = deduce(b)
        b.flags |= mines
        if safe:
            for c in safe:
                b.reveal(c)
            continue
        if mines:
            continue
        prob = probabilities(b)
        certain = [c for c, p in prob.items() if p == 0]
        sure_mines = [c for c, p in prob.items() if p == 1]
        if sure_mines:
            b.flags |= set(sure_mines)
        if certain:
            for c in certain:
                b.reveal(c)
            continue
        if sure_mines:
            continue
        # guess: the lowest-probability frontier cell, or an interior cell at the average density
        hidden = [c for c in b.cells() if c not in b.open and c not in b.flags]
        interior = [c for c in hidden if c not in prob]
        left = b.n - len(b.flags)
        density = left / max(1, len(hidden))
        pick, p = min(prob.items(), key=lambda kv: kv[1]) if prob else (None, 1.0)
        if interior and (pick is None or density < p):
            pick, p = b.rng.choice(interior), density
        guesses += 1
        if verbose:
            print(f"guess {guesses}: {pick} (p(mine)≈{p:.2f})")
        b.reveal(pick)
    if verbose:
        print(b.show(reveal_all=True))
        print("WON" if b.won else "LOST", f"after {guesses} guess(es)")
    return b.won


def play(b: Board) -> None:
    while not b.lost and not b.won:
        print(b.show())
        cmd = input("x y to open, f x y to flag, q to quit: ").split()
        if not cmd or cmd[0] == "q":
            return
        try:
            if cmd[0] == "f":
                c = (int(cmd[1]), int(cmd[2]))
                b.flags ^= {c}
            else:
                b.reveal((int(cmd[0]), int(cmd[1])))
        except (ValueError, IndexError):
            print("?")
    print(b.show(reveal_all=True))
    print("You win!" if b.won else "Boom!")


def arg(name: str, default: int) -> int:
    return int(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def main() -> None:
    size, mines = arg("--size", 16), arg("--mines", 40)
    if "--play" in sys.argv:
        play(Board(size, size, mines, random.Random()))
        return
    games = arg("--games", 0)
    if games:
        rng = random.Random(1)
        wins = sum(autoplay(Board(size, size, mines, rng)) for _ in range(games))
        print(f"{wins}/{games} boards cleared ({wins / games:.0%}) at {size}×{size} with {mines} mines")
        return
    autoplay(Board(size, size, mines, random.Random()), verbose=True)


if __name__ == "__main__":
    main()
