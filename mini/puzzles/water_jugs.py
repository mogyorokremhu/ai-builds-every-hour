"""Water jug puzzles (Die Hard 3 style) solved with breadth-first search.

You have jugs of given capacities, a tap and a drain. Each step you may fill a jug, empty
it, or pour one jug into another until the source is empty or the target is full. Find the
shortest sequence of steps that leaves exactly ``goal`` litres in some jug.

Run: python water_jugs.py [goal] [cap1 cap2 ...]     default: 4 litres with jugs 3 and 5
     python water_jugs.py 6 4 9
"""
from __future__ import annotations

import sys
from collections import deque
from math import gcd
from functools import reduce

State = tuple[int, ...]


def steps(state: State, caps: tuple[int, ...]):
    """Yield (description, next_state) for every legal action."""
    n = len(caps)
    for i in range(n):
        if state[i] < caps[i]:
            s = list(state)
            s[i] = caps[i]
            yield f"fill jug {i + 1}", tuple(s)
        if state[i] > 0:
            s = list(state)
            s[i] = 0
            yield f"empty jug {i + 1}", tuple(s)
        for j in range(n):
            if i != j and state[i] > 0 and state[j] < caps[j]:
                amount = min(state[i], caps[j] - state[j])
                s = list(state)
                s[i] -= amount
                s[j] += amount
                yield f"pour jug {i + 1} into jug {j + 1}", tuple(s)


def solve(goal: int, caps: tuple[int, ...]) -> list[tuple[str, State]] | None:
    start: State = (0,) * len(caps)
    prev: dict[State, tuple[State, str] | None] = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        if goal in cur:
            path = []
            while prev[cur] is not None:
                before, what = prev[cur]
                path.append((what, cur))
                cur = before
            return path[::-1]
        for what, nxt in steps(cur, caps):
            if nxt not in prev:
                prev[nxt] = (cur, what)
                q.append(nxt)
    return None


def main() -> None:
    args = [int(a) for a in sys.argv[1:]]
    goal = args[0] if args else 4
    caps = tuple(args[1:]) or (3, 5)
    print(f"Measure {goal} L with jugs of {', '.join(map(str, caps))} L")
    if goal > max(caps) or goal % reduce(gcd, caps):
        print("Impossible: the goal must be a multiple of the jugs' gcd and fit in a jug.")
        return
    path = solve(goal, caps)
    if path is None:
        print("No solution.")
        return
    for n, (what, state) in enumerate(path, 1):
        jugs = "  ".join(f"[{v:>2}/{c}]" for v, c in zip(state, caps))
        print(f"{n:>2}. {what:<24} {jugs}")
    print(f"Done in {len(path)} steps.")


if __name__ == "__main__":
    main()
