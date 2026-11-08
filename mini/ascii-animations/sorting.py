#!/usr/bin/env python3
"""Sorting algorithms racing as animated bar charts: compares glow, swaps flash, counters tick.

Usage: python sorting.py [--algo bubble|insertion|selection|shell|quick|heap|merge|all]
                         [--size N] [--height H] [--fps F] [--frames N] [--seed S] [--no-color]
Each algorithm is a generator that yields ("cmp", i, j) / ("set", i, value) events, so the
animation shows exactly the work the algorithm does.
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from collections.abc import Callable, Iterator

Event = tuple[str, int, int]


def bubble(a: list[int]) -> Iterator[Event]:
    """Bubble sort with early exit."""
    n = len(a)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            yield ("cmp", i, i + 1)
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                yield ("set", i, a[i])
                yield ("set", i + 1, a[i + 1])
                swapped = True
        if not swapped:
            return


def insertion(a: list[int]) -> Iterator[Event]:
    """Insertion sort (shifting)."""
    for i in range(1, len(a)):
        v, j = a[i], i - 1
        while j >= 0:
            yield ("cmp", j, i)
            if a[j] <= v:
                break
            a[j + 1] = a[j]
            yield ("set", j + 1, a[j + 1])
            j -= 1
        a[j + 1] = v
        yield ("set", j + 1, v)


def selection(a: list[int]) -> Iterator[Event]:
    """Selection sort."""
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            yield ("cmp", m, j)
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
            yield ("set", i, a[i])
            yield ("set", m, a[m])


def shell(a: list[int]) -> Iterator[Event]:
    """Shell sort with Ciura's gap sequence."""
    gaps = [g for g in (701, 301, 132, 57, 23, 10, 4, 1) if g < len(a)] or [1]
    for gap in gaps:
        for i in range(gap, len(a)):
            v, j = a[i], i
            while j >= gap:
                yield ("cmp", j - gap, i)
                if a[j - gap] <= v:
                    break
                a[j] = a[j - gap]
                yield ("set", j, a[j])
                j -= gap
            a[j] = v
            yield ("set", j, v)


def quick(a: list[int]) -> Iterator[Event]:
    """Quicksort (Lomuto partition, median-of-three pivot, explicit stack)."""
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        mid = (lo + hi) // 2
        trio = sorted([(a[lo], lo), (a[mid], mid), (a[hi], hi)])
        p = trio[1][1]
        a[p], a[hi] = a[hi], a[p]
        yield ("set", p, a[p])
        yield ("set", hi, a[hi])
        pivot, store = a[hi], lo
        for i in range(lo, hi):
            yield ("cmp", i, hi)
            if a[i] < pivot:
                a[i], a[store] = a[store], a[i]
                yield ("set", i, a[i])
                yield ("set", store, a[store])
                store += 1
        a[store], a[hi] = a[hi], a[store]
        yield ("set", store, a[store])
        yield ("set", hi, a[hi])
        stack += [(lo, store - 1), (store + 1, hi)]


def heap(a: list[int]) -> Iterator[Event]:
    """Heapsort (max-heap, sift-down)."""
    n = len(a)

    def sift(start: int, end: int) -> Iterator[Event]:
        root = start
        while 2 * root + 1 <= end:
            child = 2 * root + 1
            if child + 1 <= end:
                yield ("cmp", child, child + 1)
                if a[child] < a[child + 1]:
                    child += 1
            yield ("cmp", root, child)
            if a[root] >= a[child]:
                return
            a[root], a[child] = a[child], a[root]
            yield ("set", root, a[root])
            yield ("set", child, a[child])
            root = child

    for start in range(n // 2 - 1, -1, -1):
        yield from sift(start, n - 1)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        yield ("set", 0, a[0])
        yield ("set", end, a[end])
        yield from sift(0, end - 1)


def merge(a: list[int]) -> Iterator[Event]:
    """Bottom-up merge sort writing merged runs back into the array."""
    n, width = len(a), 1
    while width < n:
        for lo in range(0, n, 2 * width):
            mid, hi = min(lo + width, n), min(lo + 2 * width, n)
            left, right = a[lo:mid], a[mid:hi]
            i = j = 0
            k = lo
            while i < len(left) and j < len(right):
                yield ("cmp", lo + i, mid + j)
                if left[i] <= right[j]:
                    a[k] = left[i]
                    i += 1
                else:
                    a[k] = right[j]
                    j += 1
                yield ("set", k, a[k])
                k += 1
            for v in left[i:] + right[j:]:
                a[k] = v
                yield ("set", k, v)
                k += 1
        width *= 2


ALGOS: dict[str, Callable[[list[int]], Iterator[Event]]] = {
    "bubble": bubble, "insertion": insertion, "selection": selection, "shell": shell,
    "quick": quick, "heap": heap, "merge": merge,
}
BLOCKS = " ▁▂▃▄▅▆▇█"


def bars(values: list[int], height: int, hot: dict[int, str], color: bool) -> list[str]:
    """Render values (1..max) as vertical bars `height` rows tall with eighth-block tops."""
    top = max(values) or 1
    rows = []
    for row in range(height, 0, -1):
        line = []
        for i, v in enumerate(values):
            level = v * height * 8 // top - (row - 1) * 8
            ch = BLOCKS[max(0, min(8, level))]
            if color and i in hot and ch != " ":
                line.append(f"{hot[i]}{ch}\x1b[0m")
            else:
                line.append(ch)
        rows.append("".join(line))
    return rows


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--algo", default="all", choices=[*ALGOS, "all"])
    ap.add_argument("--size", type=int, default=60)
    ap.add_argument("--height", type=int, default=16)
    ap.add_argument("--fps", type=float, default=60)
    ap.add_argument("--frames", type=int, default=0, help="stop after N frames (0 = until sorted)")
    ap.add_argument("--steps", type=int, default=0, help="events per frame (0 = auto)")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    names = list(ALGOS) if a.algo == "all" else [a.algo]
    frame = 0
    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        for name in names:
            values = list(range(1, a.size + 1))
            rng.shuffle(values)
            shown = values[:]          # what is on screen (updated from events only)
            work = values[:]           # the array the algorithm sorts
            gen = ALGOS[name](work)
            cmps = writes = 0
            per_frame = a.steps or max(1, a.size * a.size // 600)
            done = False
            while not done:
                hot: dict[int, str] = {}
                for _ in range(per_frame):
                    ev = next(gen, None)
                    if ev is None:
                        done = True
                        break
                    kind, i, j = ev
                    if kind == "cmp":
                        cmps += 1
                        hot[i] = hot[j] = "\x1b[38;5;220m"
                    else:
                        writes += 1
                        shown[i] = j
                        hot[i] = "\x1b[38;5;203m"
                if done:
                    hot = {i: "\x1b[38;5;114m" for i in range(len(shown))}
                screen = bars(shown, a.height, hot, not a.no_color)
                screen.append(f"{name:<10} n={a.size}  comparisons {cmps:>6}  writes {writes:>6}" + ("  ✓ sorted" if done else ""))
                sys.stdout.write("\x1b[H" + "\n".join(screen) + "\x1b[K")
                sys.stdout.flush()
                frame += 1
                if a.frames and frame >= a.frames:
                    return
                time.sleep(1 / a.fps)
            assert shown == sorted(values), f"{name} produced an unsorted display"
            time.sleep(0.6 if not a.frames else 0)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")


if __name__ == "__main__":
    main()
