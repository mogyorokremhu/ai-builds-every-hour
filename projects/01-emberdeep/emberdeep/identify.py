"""Unidentified potions and scrolls.

Every run shuffles a set of *appearances* ("a murky potion", 'a scroll labelled "ZUN VEX"')
onto the potion and scroll kinds. Until you use one (or otherwise learn what it is), an item
shows only its appearance. Identifying a kind reveals every item of that kind at once — in
your pack and lying on the floor.

Items carry their mask in :attr:`Item.unknown_name`, so the inventory, the look command and
save files need no extra plumbing: identification simply clears the field.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Iterable

from .items import ITEM_TEMPLATES, Item

POTION_LOOKS = (
    "murky", "bubbling", "smoky", "glowing", "viscous", "fizzy", "golden", "inky", "milky",
    "crimson", "violet", "sparkling", "oily", "icy", "amber",
)
SCROLL_SYLLABLES = (
    "zun", "vex", "kor", "ath", "mel", "dra", "osh", "ith", "bal", "nyr", "qua", "tor", "elm",
    "fae", "gor", "hul", "ixx", "jor", "lum", "pex",
)

#: Kinds that are well known to every adventurer from the start.
ALWAYS_KNOWN = frozenset({"healing potion"})


def maskable_keys() -> list[str]:
    """Item keys that can be unidentified (all potions and scrolls), in a stable order."""
    return sorted(k for k, t in ITEM_TEMPLATES.items() if t.kind in ("potion", "scroll"))


def _scroll_label(rng: random.Random, taken: set[str]) -> str:
    while True:
        words = [rng.choice(SCROLL_SYLLABLES) + rng.choice(SCROLL_SYLLABLES)
                 for _ in range(rng.randint(1, 2))]
        label = " ".join(words).upper()
        if label not in taken:
            taken.add(label)
            return label


@dataclass
class Identification:
    """Per-run table of appearances plus the set of kinds the player has identified."""

    appearances: dict[str, str] = field(default_factory=dict)
    known: set[str] = field(default_factory=set)

    @classmethod
    def roll(cls, rng: random.Random) -> "Identification":
        """Shuffle appearances for a new run (uses its own RNG so the dungeon is unaffected)."""
        looks = list(POTION_LOOKS)
        rng.shuffle(looks)
        labels: set[str] = set()
        table: dict[str, str] = {}
        for key in maskable_keys():
            if ITEM_TEMPLATES[key].kind == "potion":
                table[key] = f"{looks.pop()} potion"
            else:
                table[key] = f'scroll labelled "{_scroll_label(rng, labels)}"'
        return cls(table, set(ALWAYS_KNOWN))

    @classmethod
    def everything_known(cls) -> "Identification":
        """Used for old save files written before identification existed."""
        return cls({}, set(maskable_keys()))

    def is_known(self, key: str) -> bool:
        return key in self.known or key not in self.appearances

    def mask(self, item: Item) -> Item:
        """Hide ``item``'s identity if its kind is still unknown (returns the item)."""
        item.unknown_name = None if self.is_known(item.key) else self.appearances[item.key]
        return item

    def identify(self, key: str, items: Iterable[Item]) -> bool:
        """Mark ``key`` known and unmask matching ``items``. Returns True if it was new."""
        new = not self.is_known(key)
        self.known.add(key)
        for it in items:
            if it.key == key:
                it.unknown_name = None
        return new

    def unknown_kinds(self) -> list[str]:
        return sorted(k for k in self.appearances if k not in self.known)

    def discoveries(self) -> list[tuple[str, str]]:
        """(appearance, real name) for every identified maskable kind, for the morgue/help."""
        return [(self.appearances[k], ITEM_TEMPLATES[k].name) for k in sorted(self.known)
                if k in self.appearances]

    def to_dict(self) -> dict:
        return {"appearances": dict(self.appearances), "known": sorted(self.known)}

    @classmethod
    def from_dict(cls, d: dict | None) -> "Identification":
        if not d:
            return cls.everything_known()
        return cls(dict(d["appearances"]), set(d["known"]))
