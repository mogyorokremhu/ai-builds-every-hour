"""Experience levels and level-up stat choices.

Killing monsters grants XP. Crossing a threshold queues a *pending* level-up; the UI then
asks the player to pick one of :data:`CHOICES`. Every level also grants a small automatic
HP increase, so even a careless choice keeps you growing.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .entities import Fighter

MAX_LEVEL = 20
AUTO_HP_PER_LEVEL = 2


@dataclass(frozen=True)
class Choice:
    key: str
    label: str
    description: str
    hp: int = 0
    power: int = 0
    defense: int = 0


#: Stat choices offered on every level-up, keyed by the letter the player presses.
CHOICES: dict[str, Choice] = {
    "v": Choice("v", "Vitality", "+8 max HP and heal fully", hp=8),
    "m": Choice("m", "Might", "+1 power", power=1),
    "g": Choice("g", "Guard", "+1 defense", defense=1),
}


def xp_to_next(level: int) -> int:
    """XP needed to go from ``level`` to ``level + 1`` (grows a little faster than linearly).

    Tuned with the balance bot (see BALANCE.md): the old linear curve let a thorough player
    hit the level cap well before the Ember Guardian."""
    return 40 + 35 * (level - 1) + 4 * (level - 1) ** 2


def xp_for_level(level: int) -> int:
    """Total XP needed to *reach* ``level`` (level 1 needs 0)."""
    return sum(xp_to_next(lv) for lv in range(1, level))


def level_for_xp(xp: int) -> int:
    level = 1
    while level < MAX_LEVEL and xp >= xp_for_level(level + 1):
        level += 1
    return level


class Progression:
    """Tracks XP, the current level and how many stat choices are still owed."""

    def __init__(self) -> None:
        self.xp = 0
        self.level = 1
        self.pending = 0
        self.history: list[str] = []  # choice keys taken, in order

    def gain(self, amount: int) -> int:
        """Add XP. Returns how many levels were gained."""
        self.xp += max(0, amount)
        new_level = level_for_xp(self.xp)
        gained = new_level - self.level
        if gained > 0:
            self.level = new_level
            self.pending += gained
        return gained

    @property
    def progress(self) -> tuple[int, int]:
        """(XP into the current level, XP span of the current level)."""
        if self.level >= MAX_LEVEL:
            return (1, 1)
        base = xp_for_level(self.level)
        return self.xp - base, xp_to_next(self.level)

    def apply(self, key: str, fighter: "Fighter") -> Choice:
        """Spend one pending level-up on choice ``key``. Raises ValueError if not allowed."""
        if self.pending <= 0:
            raise ValueError("no level-up pending")
        choice = CHOICES.get(key)
        if choice is None:
            raise ValueError(f"unknown choice {key!r}")
        self.pending -= 1
        self.history.append(key)
        fighter.base_max_hp += choice.hp + AUTO_HP_PER_LEVEL
        fighter.base_power += choice.power
        fighter.base_defense += choice.defense
        if choice.hp:
            fighter.hp = fighter.max_hp
        else:
            fighter.heal(AUTO_HP_PER_LEVEL)
        return choice
