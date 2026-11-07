"""Binary space partitioning (BSP) dungeon generator.

The map is split recursively into two parts (horizontally or vertically, preferring to
cut the longer side) until the leaves are small. Each leaf gets a room of random size,
and every split connects its two halves with a corridor, so the whole level is always
connected. Corridors entering a room through its wall become doors.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

from .dungeon import carve_room, carve_tunnel
from .gamemap import GameMap
from .geometry import Rect
from .tiles import DOOR, FLOOR, STAIRS_DOWN


@dataclass
class Node:
    rect: Rect
    left: "Node | None" = None
    right: "Node | None" = None
    room: Rect | None = None
    children_rooms: list[Rect] = field(default_factory=list)

    @property
    def is_leaf(self) -> bool:
        return self.left is None


def split(node: Node, rng: random.Random, min_leaf: int, depth: int = 0) -> None:
    r = node.rect
    if depth > 6:
        return
    can_h = r.h >= 2 * min_leaf
    can_v = r.w >= 2 * min_leaf
    if not (can_h or can_v):
        return
    # stop splitting some mid-sized leaves for variety
    if depth >= 3 and r.w < min_leaf * 3 and r.h < min_leaf * 3 and rng.random() < 0.25:
        return
    if can_h and can_v:
        horizontal = r.h > r.w * 0.6 if rng.random() < 0.8 else rng.random() < 0.5
    else:
        horizontal = can_h
    if horizontal:
        cut = rng.randint(min_leaf, r.h - min_leaf)
        node.left = Node(Rect(r.x, r.y, r.w, cut))
        node.right = Node(Rect(r.x, r.y + cut, r.w, r.h - cut))
    else:
        cut = rng.randint(min_leaf, r.w - min_leaf)
        node.left = Node(Rect(r.x, r.y, cut, r.h))
        node.right = Node(Rect(r.x + cut, r.y, r.w - cut, r.h))
    split(node.left, rng, min_leaf, depth + 1)
    split(node.right, rng, min_leaf, depth + 1)


def leaves(node: Node) -> list[Node]:
    if node.is_leaf:
        return [node]
    return leaves(node.left) + leaves(node.right)  # type: ignore[arg-type]


def any_room(node: Node, rng: random.Random) -> Rect:
    rooms = [lf.room for lf in leaves(node) if lf.room is not None]
    return rng.choice(rooms)


def place_doors(gmap: GameMap, rooms: list[Rect], rng: random.Random, chance: float = 0.6) -> int:
    """Turn corridor openings in room walls into doors. Returns the number placed."""
    placed = 0
    for room in rooms:
        border = [(x, room.y) for x in range(room.x + 1, room.x2 - 1)]
        border += [(x, room.y2 - 1) for x in range(room.x + 1, room.x2 - 1)]
        vertical = [(room.x, y) for y in range(room.y + 1, room.y2 - 1)]
        vertical += [(room.x2 - 1, y) for y in range(room.y + 1, room.y2 - 1)]
        for (x, y), along in [(p, (1, 0)) for p in border] + [(p, (0, 1)) for p in vertical]:
            if gmap.get(x, y).name != "floor":
                continue
            ax, ay = along
            if gmap.walkable(x - ax, y - ay) or gmap.walkable(x + ax, y + ay):
                continue  # wide opening, not a doorway
            if any(gmap.get(x + dx, y + dy).name == "door" for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                continue
            if rng.random() < chance:
                gmap.set(x, y, DOOR)
                placed += 1
    return placed


def generate(width: int, height: int, rng: random.Random, min_leaf: int = 7,
             doors: bool = True) -> tuple[GameMap, list[Rect]]:
    """Generate a BSP dungeon. Returns the map and its rooms (first = start, last = stairs)."""
    gmap = GameMap(width, height)
    root = Node(Rect(0, 0, width, height))
    split(root, rng, min_leaf)
    rooms: list[Rect] = []
    for lf in leaves(root):
        r = lf.rect
        w = rng.randint(max(5, r.w * 2 // 3), max(5, r.w - 1))
        h = rng.randint(max(5, r.h * 2 // 3), max(5, r.h - 1))
        w, h = min(w, r.w - 1), min(h, r.h - 1)
        if w < 4 or h < 4:
            continue
        x = rng.randint(r.x, r.x + r.w - w - 1) if r.w - w - 1 > 0 else r.x
        y = rng.randint(r.y, r.y + r.h - h - 1) if r.h - h - 1 > 0 else r.y
        room = Rect(x, y, w, h)
        lf.room = room
        carve_room(gmap, room)
        rooms.append(room)

    def connect(node: Node) -> None:
        if node.is_leaf:
            return
        connect(node.left)   # type: ignore[arg-type]
        connect(node.right)  # type: ignore[arg-type]
        has_l = any(lf.room for lf in leaves(node.left))   # type: ignore[arg-type]
        has_r = any(lf.room for lf in leaves(node.right))  # type: ignore[arg-type]
        if has_l and has_r:
            a = any_room(node.left, rng).center   # type: ignore[arg-type]
            b = any_room(node.right, rng).center  # type: ignore[arg-type]
            carve_tunnel(gmap, a, b, rng)

    connect(root)
    if doors:
        place_doors(gmap, rooms, rng)
    if rooms:
        # start in the first room, stairs in the room farthest from it
        sx, sy = rooms[0].center
        far = max(rooms[1:] or rooms, key=lambda rm: abs(rm.center[0] - sx) + abs(rm.center[1] - sy))
        rooms.remove(far)
        rooms.append(far)
        gmap.set(*far.center, STAIRS_DOWN)
        gmap.stairs = far.center
        gmap.set(sx, sy, FLOOR)
    return gmap, rooms
