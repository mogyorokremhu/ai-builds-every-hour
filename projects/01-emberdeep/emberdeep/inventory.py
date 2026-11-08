"""Letter-indexed inventory (a–z) with stacking of identical consumables."""
from __future__ import annotations

import string

from .items import Item

LETTERS = string.ascii_lowercase


class Inventory:
    """The player's pack: up to ``capacity`` lettered item slots, with stacking."""
    def __init__(self, capacity: int = 26) -> None:
        self.capacity = min(capacity, len(LETTERS))
        self.items: list[Item] = []

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    @property
    def full(self) -> bool:
        """True if every slot is taken."""
        return len(self.items) >= self.capacity

    def can_add(self, item: Item) -> bool:
        """True if ``item`` fits, in a free slot or on an existing stack."""
        return not self.full or self._stack_target(item) is not None

    def _stack_target(self, item: Item) -> Item | None:
        if not item.stackable:
            return None
        for it in self.items:
            if it.key == item.key and it.stackable:
                return it
        return None

    def add(self, item: Item) -> bool:
        """Add an item, merging stacks. Returns False if there is no room."""
        target = self._stack_target(item)
        if target is not None:
            target.count += item.count
            return True
        if self.full:
            return False
        self.items.append(item)
        return True

    def take_one(self, item: Item) -> Item:
        """Remove one unit of ``item`` and return it (splitting stacks)."""
        from dataclasses import replace

        if item.count > 1:
            item.count -= 1
            return replace(item, count=1)
        self.remove(item)
        return item

    def _index(self, item: Item) -> int:
        for i, it in enumerate(self.items):
            if it is item:
                return i
        raise ValueError(f"{item.name} is not in the inventory")

    def remove(self, item: Item) -> None:
        """Remove this exact item (the whole stack) from the pack."""
        del self.items[self._index(item)]

    def letter_of(self, item: Item) -> str:
        """The inventory letter of ``item``."""
        return LETTERS[self._index(item)]

    def get(self, letter: str) -> Item | None:
        """The item under inventory ``letter``, or None."""
        idx = LETTERS.find(letter)
        if 0 <= idx < len(self.items):
            return self.items[idx]
        return None

    def listing(self) -> list[tuple[str, Item]]:
        """(letter, item) pairs for every item in the pack."""
        return [(LETTERS[i], it) for i, it in enumerate(self.items)]
