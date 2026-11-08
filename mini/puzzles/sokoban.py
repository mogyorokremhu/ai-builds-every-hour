#!/usr/bin/env python3
"""Sokoban: play in the terminal, or let the solver find the fewest pushes.

The solver searches over *push* states (box positions + the region the player can
reach), so walking around is free and only pushes count. It uses A* with a
lower bound of the sum of each box's distance to its nearest goal, and prunes
"dead squares" — floor cells from which a box can never reach any goal
(computed once by pulling boxes backwards from the goals).

    python sokoban.py              # solve level 1 and replay the solution
    python sokoban.py --level 2    # another built-in level
    python sokoban.py --play       # play: w/a/s/d to move, u to undo, r to restart, q to quit

Level symbols: # wall, . goal, $ box, * box on goal, @ player, + player on goal.
"""
from __future__ import annotations

import heapq
import sys
from collections import deque

LEVELS = [
    """\
  #####
###   #
#.@$  #
### $.#
#.##$ #
# # . ##
#$ *$$.#
#   .  #
########""",
    """\
#######
#     #
# $$$ #
#.@   #
# ... #
#######""",
    """\
 ######
 #    #
 # #@ #
 # $* #
 # .* #
 #    #
 ######""",
]

DIRS = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}


class Level:
    def __init__(self, text: str):
        rows = text.split("\n")
        self.h, self.w = len(rows), max(len(r) for r in rows)
        self.walls, self.goals, boxes = set(), set(), set()
        self.player = (0, 0)
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                if ch == "#":
                    self.walls.add((r, c))
                if ch in ".*+":
                    self.goals.add((r, c))
                if ch in "$*":
                    boxes.add((r, c))
                if ch in "@+":
                    self.player = (r, c)
        self.boxes = frozenset(boxes)
        self.floor = self._floor()
        self.live = self._live_squares()

    def _floor(self) -> set[tuple[int, int]]:
        seen, todo = {self.player}, [self.player]
        while todo:
            r, c = todo.pop()
            for dr, dc in DIRS.values():
                n = (r + dr, c + dc)
                if n not in self.walls and n not in seen and 0 <= n[0] < self.h and 0 <= n[1] < self.w:
                    seen.add(n)
                    todo.append(n)
        return seen

    def _live_squares(self) -> set[tuple[int, int]]:
        """Squares from which a box can still be pushed onto some goal (reverse 'pulls')."""
        live, todo = set(self.goals), deque(self.goals)
        while todo:
            r, c = todo.popleft()
            for dr, dc in DIRS.values():
                box, player = (r + dr, c + dc), (r + 2 * dr, c + 2 * dc)
                if box in self.floor and player in self.floor and box not in live:
                    live.add(box)
                    todo.append(box)
        return live

    def reach(self, player, boxes) -> set[tuple[int, int]]:
        seen, todo = {player}, [player]
        while todo:
            r, c = todo.pop()
            for dr, dc in DIRS.values():
                n = (r + dr, c + dc)
                if n in self.floor and n not in boxes and n not in seen:
                    seen.add(n)
                    todo.append(n)
        return seen

    def heuristic(self, boxes) -> int:
        return sum(min(abs(b[0] - g[0]) + abs(b[1] - g[1]) for g in self.goals) for b in boxes)

    def solve(self, limit: int = 300_000):
        """Fewest-push solution as a list of (box, direction) pushes, or None."""
        start_reach = self.reach(self.player, self.boxes)
        key = lambda boxes, reach: (boxes, min(reach))
        start = (self.boxes, self.player)
        best = {key(self.boxes, start_reach): 0}
        parent = {key(self.boxes, start_reach): None}
        heap = [(self.heuristic(self.boxes), 0, 0, start)]
        tie = 0
        while heap and len(best) < limit:
            _, g, _, (boxes, player) = heapq.heappop(heap)
            reach = self.reach(player, boxes)
            k = key(boxes, reach)
            if best.get(k, 1e9) < g:
                continue
            if boxes <= self.goals:
                path = []
                while parent[k]:
                    k, push = parent[k]
                    path.append(push)
                return path[::-1]
            for b in boxes:
                for name, (dr, dc) in DIRS.items():
                    stand, dest = (b[0] - dr, b[1] - dc), (b[0] + dr, b[1] + dc)
                    if stand not in reach or dest not in self.live or dest in boxes:
                        continue
                    nb = (boxes - {b}) | {dest}
                    nreach = self.reach(b, nb)
                    nk = key(nb, nreach)
                    if best.get(nk, 1e9) <= g + 1:
                        continue
                    best[nk] = g + 1
                    parent[nk] = (k, (b, name))
                    tie += 1
                    heapq.heappush(heap, (g + 1 + self.heuristic(nb), g + 1, tie, (nb, b)))
        return None

    def draw(self, player, boxes) -> str:
        out = []
        for r in range(self.h):
            row = ""
            for c in range(self.w):
                p = (r, c)
                if p in self.walls:
                    row += "#"
                elif p in boxes:
                    row += "*" if p in self.goals else "$"
                elif p == player:
                    row += "+" if p in self.goals else "@"
                else:
                    row += "." if p in self.goals else " "
            out.append(row.rstrip())
        return "\n".join(out)


def walk(level: Level, start, goal, boxes) -> str:
    """Player moves (w/a/s/d) from start to goal avoiding boxes (BFS)."""
    prev = {start: None}
    todo = deque([start])
    while todo:
        cur = todo.popleft()
        if cur == goal:
            break
        for name, (dr, dc) in DIRS.items():
            n = (cur[0] + dr, cur[1] + dc)
            if n in level.floor and n not in boxes and n not in prev:
                prev[n] = (cur, name)
                todo.append(n)
    moves = []
    cur = goal
    while prev[cur]:
        cur, name = prev[cur]
        moves.append(name)
    return "".join(reversed(moves))


def replay(level: Level, pushes) -> str:
    """Expand pushes into a full move string and print a few frames."""
    player, boxes = level.player, set(level.boxes)
    keys = ""
    for box, name in pushes:
        dr, dc = DIRS[name]
        keys += walk(level, player, (box[0] - dr, box[1] - dc), boxes) + name.upper()
        boxes.remove(box)
        boxes.add((box[0] + dr, box[1] + dc))
        player = box
    print(level.draw(player, boxes))
    return keys


def play(level: Level) -> None:
    player, boxes, history = level.player, set(level.boxes), []
    while True:
        print("\n" + level.draw(player, boxes))
        if boxes <= level.goals:
            print(f"Solved in {len(history)} moves!")
            return
        cmd = input("move (w/a/s/d, u undo, r restart, q quit): ").strip().lower()
        if cmd == "q":
            return
        if cmd == "r":
            player, boxes, history = level.player, set(level.boxes), []
            continue
        if cmd == "u" and history:
            player, boxes = history.pop()
            continue
        for ch in cmd:
            if ch not in DIRS:
                continue
            dr, dc = DIRS[ch]
            n = (player[0] + dr, player[1] + dc)
            if n not in level.floor:
                continue
            if n in boxes:
                beyond = (n[0] + dr, n[1] + dc)
                if beyond not in level.floor or beyond in boxes:
                    continue
                history.append((player, set(boxes)))
                boxes.remove(n)
                boxes.add(beyond)
            else:
                history.append((player, set(boxes)))
            player = n


def main() -> None:
    idx = int(sys.argv[sys.argv.index("--level") + 1]) - 1 if "--level" in sys.argv else 0
    level = Level(LEVELS[idx])
    print(level.draw(level.player, level.boxes))
    if "--play" in sys.argv:
        play(level)
        return
    pushes = level.solve()
    if pushes is None:
        print("No solution found.")
        return
    print(f"\nSolved with {len(pushes)} pushes. Final position:")
    keys = replay(level, pushes)
    print(f"Moves ({len(keys)}; capitals are pushes):\n{keys}")


if __name__ == "__main__":
    main()
