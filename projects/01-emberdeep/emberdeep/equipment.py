"""Equipment slots (weapon, armor, ring) and their stat bonuses."""
from __future__ import annotations

from .entities import Fighter
from .items import Item

SLOTS = ("weapon", "armor", "ring")


class Equipment:
    def __init__(self) -> None:
        self.slots: dict[str, Item | None] = {s: None for s in SLOTS}

    def is_equipped(self, item: Item) -> bool:
        return any(it is item for it in self.slots.values())

    def equip(self, item: Item) -> Item | None:
        """Put ``item`` in its slot. Returns the item that was replaced (if any)."""
        if item.slot not in self.slots:
            raise ValueError(f"{item.name} cannot be equipped")
        old = self.slots[item.slot]
        self.slots[item.slot] = item
        return old

    def unequip(self, item: Item) -> bool:
        for slot, it in self.slots.items():
            if it is item:
                self.slots[slot] = None
                return True
        return False

    def bonus(self, attr: str) -> int:
        return sum(getattr(it, attr) for it in self.slots.values() if it is not None)

    def apply_to(self, fighter: Fighter) -> None:
        """Recompute the fighter's bonus stats from what is worn, clamping HP."""
        fighter.bonus_power = self.bonus("power_bonus")
        fighter.bonus_defense = self.bonus("defense_bonus")
        fighter.bonus_hp = self.bonus("hp_bonus")
        fighter.hp = min(fighter.hp, fighter.max_hp)
