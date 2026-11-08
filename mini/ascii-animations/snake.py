#!/usr/bin/env python3
"""A self-playing Snake: BFS to the food, falling back to chasing its own tail when boxed in.

Usage: python snake.py [--frames N] [--width 30] [--height 14] [--fps 15] [--seed S]
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from collections import deque

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def bfs(start, goal, blocked, w, h):
    """First step of a shortest path from start to goal avoiding `blocked`, or None."""
    prev = {start: None}
    q = deque([start])
    while q:
        c = q.popleft()
        if c == goal:
            while prev[c] != start and prev[c] is not None:
                c = prev[c]
            return c if prev[c] is not None or c != start else None
        for dx, dy in DIRS:
            n = (c[0] + dx, c[1] + dy)
            if 0 <= n[0] < w and 0 <= n[1] < h and n not in blocked and n not in prev:
                prev[n] = c
                q.append(n)
    return None


def choose_step(snake, food, w, h):
    """Next head cell: toward food if a path exists (and the tail stays reachable), else toward the tail, else any safe cell."""
    head, body = snake[0], set(snake[:-1])
    step = bfs(head, food, body, w, h)
    if step is not None:
        # simulate eating: after the move the snake must still be able to reach its tail
        sim = [step] + snake[:] if step == food else [step] + snake[:-1]
        if bfs(sim[0], sim[-1], set(sim[1:-1]), w, h) is not None or len(sim) <= 3:
            return step
    tail_step = bfs(head, snake[-1], set(snake[:-1]) - {snake[-1]}, w, h)
    if tail_step is not None and tail_step not in body:
        return tail_step
    for dx, dy in DIRS:
        n = (head[0] + dx, head[1] + dy)
        if 0 <= n[0] < w and 0 <= n[1] < h and n not in body:
            return n
    return None


class Game:
    def __init__(self, w, h, rng):
        self.w, self.h, self.rng = w, h, rng
        self.reset()

    def reset(self):
        self.snake = [(self.w // 2, self.h // 2)]
        self.score = 0
        self.food = self.place_food()

    def place_food(self):
        free = [(x, y) for x in range(self.w) for y in range(self.h) if (x, y) not in self.snake]
        return self.rng.choice(free) if free else None

    def step(self):
        if self.food is None:
            self.reset()
            return
        nxt = choose_step(self.snake, self.food, self.w, self.h)
        if nxt is None:
            self.reset()
            return
        self.snake.insert(0, nxt)
        if nxt == self.food:
            self.score += 1
            self.food = self.place_food()
        else:
            self.snake.pop()

    def render(self):
        rows = []
        for y in range(self.h):
            row = []
            for x in range(self.w):
                c = (x, y)
                row.append("@" if c == self.snake[0] else "o" if c in self.snake else "*" if c == self.food else "·")
            rows.append("".join(row))
        return "\n".join(rows) + f"\nscore {self.score}  length {len(self.snake)}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=30)
    ap.add_argument("--height", type=int, default=14)
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args(argv)
    g = Game(a.width, a.height, random.Random(a.seed))
    n = 0
    try:
        sys.stdout.write("\x1b[2J\x1b[?25l")
        while not a.frames or n < a.frames:
            g.step()
            sys.stdout.write("\x1b[H" + g.render() + "\n")
            sys.stdout.flush()
            time.sleep(1 / a.fps)
            n += 1
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")


if __name__ == "__main__":
    main()
