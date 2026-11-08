"""Depth-aware loot tables."""
from __future__ import annotations

import random

from .items import Item, make_item

#: (item key, min depth, max depth, weight)
LOOT_TABLE: list[tuple[str, int, int, int]] = [
    ("healing potion", 1, 99, 28),
    ("greater healing potion", 4, 99, 12),
    ("speed potion", 2, 99, 6),
    ("fire potion", 2, 99, 6),
    ("venom potion", 3, 99, 4),
    ("lightning scroll", 1, 99, 12),
    ("confusion scroll", 1, 99, 10),
    ("teleport scroll", 2, 99, 6),
    ("fireball scroll", 3, 99, 9),
    ("torch", 1, 99, 9),
    ("ration", 1, 99, 9),
    ("glowcap", 3, 99, 4),
    ("dagger", 1, 3, 6),
    ("leather armor", 1, 4, 6),
    ("sword", 3, 99, 5),
    ("chain mail", 3, 99, 4),
    ("war axe", 5, 99, 3),
    ("warhammer", 4, 99, 3),
    ("ember plate", 6, 99, 2),
    ("ring of strength", 4, 99, 2),
    ("ring of protection", 4, 99, 2),
    ("ring of vitality", 2, 99, 2),
]


def table_for(depth: int, bias: dict[str, float] | None = None) -> list[tuple[str, float]]:
    """Weighted pool for ``depth``; ``bias`` multiplies the weight of specific items (themes)."""
    bias = bias or {}
    return [(k, w * bias.get(k, 1.0)) for k, lo, hi, w in LOOT_TABLE if lo <= depth <= hi]


def roll_loot(depth: int, rng: random.Random, bias: dict[str, float] | None = None) -> Item:
    """Pick a random item appropriate for ``depth``."""
    pool = table_for(depth, bias)
    keys, weights = zip(*pool)
    return make_item(rng.choices(keys, weights=weights)[0])


def items_per_room(depth: int, rng: random.Random) -> int:
    """How many items a room gets: usually 0–1, a little more deeper down."""
    n = 1 if rng.random() < 0.45 else 0
    if depth >= 3 and rng.random() < 0.15:
        n += 1
    return n
