"""Pathfinding: A* for chasing, Dijkstra maps for fleeing and distance queries.

Movement is 8-directional and every step takes one turn, but diagonal steps cost
slightly more (11 vs 10) so paths look natural instead of zig-zagging.
"""
from __future__ import annotations

import heapq
from typing import Callable, Iterable

from .gamemap import GameMap

Pos = tuple[int, int]

ORTHO_COST = 10
DIAG_COST = 11
DIRECTIONS: tuple[Pos, ...] = (
    (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1),
)


def step_cost(dx: int, dy: int) -> int:
    return DIAG_COST if dx and dy else ORTHO_COST


def neighbors(gmap: GameMap, pos: Pos) -> Iterable[tuple[Pos, int]]:
    """Walkable neighbouring cells with their step cost."""
    x, y = pos
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if gmap.walkable(nx, ny):
            yield (nx, ny), step_cost(dx, dy)


def heuristic(a: Pos, b: Pos) -> int:
    """Octile distance with our step costs (admissible and consistent)."""
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return ORTHO_COST * max(dx, dy) + (DIAG_COST - ORTHO_COST) * min(dx, dy)


def astar(
    gmap: GameMap,
    start: Pos,
    goal: Pos,
    extra_cost: Callable[[int, int], int] | None = None,
    max_nodes: int = 4000,
) -> list[Pos]:
    """Return the cells to walk from ``start`` to ``goal`` (start excluded, goal included).

    ``extra_cost(x, y)`` adds a penalty to entering a cell (e.g. one occupied by another
    monster, so crowds route around each other). The goal is always enterable even if it is
    not walkable for pathing purposes. Returns ``[]`` if no path is found within
    ``max_nodes`` expansions or if start == goal.
    """
    if start == goal:
        return []
    frontier: list[tuple[int, int, Pos]] = [(heuristic(start, goal), 0, start)]
    came_from: dict[Pos, Pos] = {}
    cost_so_far: dict[Pos, int] = {start: 0}
    counter = 0
    expanded = 0
    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current == goal:
            break
        expanded += 1
        if expanded > max_nodes:
            return []
        cx, cy = current
        for dx, dy in DIRECTIONS:
            nxt = (cx + dx, cy + dy)
            if nxt != goal and not gmap.walkable(*nxt):
                continue
            new_cost = cost_so_far[current] + step_cost(dx, dy)
            if extra_cost is not None and nxt != goal:
                new_cost += extra_cost(*nxt)
            if new_cost < cost_so_far.get(nxt, 1 << 30):
                cost_so_far[nxt] = new_cost
                came_from[nxt] = current
                counter += 1
                # tie-break on counter so heap entries never compare positions first
                heapq.heappush(frontier, (new_cost + heuristic(nxt, goal), counter, nxt))
    if goal not in came_from:
        return []
    path = [goal]
    while path[-1] in came_from and came_from[path[-1]] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def dijkstra_map(gmap: GameMap, sources: Iterable[Pos], max_cost: int = 1 << 30) -> dict[Pos, int]:
    """Cost from the nearest source to every reachable walkable cell (up to ``max_cost``)."""
    dist: dict[Pos, int] = {}
    heap: list[tuple[int, Pos]] = []
    for s in sources:
        dist[s] = 0
        heap.append((0, s))
    heapq.heapify(heap)
    while heap:
        d, pos = heapq.heappop(heap)
        if d > dist.get(pos, 1 << 30) or d > max_cost:
            continue
        for nxt, c in neighbors(gmap, pos):
            nd = d + c
            if nd < dist.get(nxt, 1 << 30) and nd <= max_cost:
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return dist


def flee_map(gmap: GameMap, threat: Pos, radius: int = 20, coefficient: float = -1.2) -> dict[Pos, int]:
    """A "safety map" in the style of Brogue: lower values are safer.

    Take the distance-from-threat map, multiply by a negative coefficient and let it
    re-settle. Walking downhill moves *away* from the threat but prefers escape routes
    over dead-end corners (a plain "maximise distance" walk gets trapped in corners).
    """
    base = dijkstra_map(gmap, [threat], max_cost=radius * ORTHO_COST)
    seeded = {p: int(d * coefficient) for p, d in base.items()}
    # re-relax: every cell becomes min(own value, neighbour + step)
    heap = [(v, p) for p, v in seeded.items()]
    heapq.heapify(heap)
    result = dict(seeded)
    while heap:
        v, pos = heapq.heappop(heap)
        if v > result[pos]:
            continue
        for nxt, c in neighbors(gmap, pos):
            if nxt in result and v + c < result[nxt]:
                result[nxt] = v + c
                heapq.heappush(heap, (v + c, nxt))
    return result


def downhill_step(
    gmap: GameMap, pos: Pos, field: dict[Pos, int], blocked: Callable[[int, int], bool] | None = None
) -> Pos | None:
    """The (dx, dy) that moves to the lowest neighbouring value of ``field``, or None."""
    here = field.get(pos)
    if here is None:
        return None
    best: tuple[int, Pos] | None = None
    for (nx, ny), _ in neighbors(gmap, pos):
        if blocked is not None and blocked(nx, ny):
            continue
        v = field.get((nx, ny))
        if v is not None and v < here and (best is None or v < best[0]):
            best = (v, (nx - pos[0], ny - pos[1]))
    return best[1] if best else None
