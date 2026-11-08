"""Status effects: burning, poisoned, confused, slowed, hasted.

A :class:`StatusSet` lives on every creature. Statuses tick once per action of the
creature that carries them (so a hasted creature also shakes off effects faster).
"""
from __future__ import annotations

from dataclasses import dataclass, field

#: name -> (short label for the HUD, colour, adjective for messages, damaging?)
STATUS_INFO: dict[str, tuple[str, str, str, bool]] = {
    "burning": ("Burn", "bright_red", "on fire", True),
    "poisoned": ("Pois", "bright_green", "poisoned", True),
    "confused": ("Conf", "bright_magenta", "confused", False),
    "slowed": ("Slow", "cyan", "slowed", False),
    "hasted": ("Fast", "bright_yellow", "moving quickly", False),
}

#: Statuses that cancel each other out when applied.
OPPOSITES = {"slowed": "hasted", "hasted": "slowed"}


@dataclass
class Status:
    """One active status effect: its name, turns left and per-tick power."""
    name: str
    turns: int
    power: int = 0  # damage per tick for damaging statuses


@dataclass
class TickResult:
    """What happened when a creature's statuses ticked."""

    damage: list[tuple[str, int]] = field(default_factory=list)  # (status, amount)
    expired: list[str] = field(default_factory=list)

    @property
    def total_damage(self) -> int:
        """Sum of all damage dealt by this tick."""
        return sum(d for _, d in self.damage)


class StatusSet:
    """The set of status effects on a creature, at most one of each kind."""
    def __init__(self) -> None:
        self._s: dict[str, Status] = {}

    def add(self, name: str, turns: int, power: int = 0) -> bool:
        """Apply a status. Re-applying keeps the longer duration and stronger power.

        Returns True if this is a new status (False if it refreshed an existing one).
        Applying the opposite of an active status (haste vs slow) cancels both.
        """
        if name not in STATUS_INFO:
            raise KeyError(name)
        opp = OPPOSITES.get(name)
        if opp and opp in self._s:
            del self._s[opp]
            return False
        if turns <= 0:
            self._s.pop(name, None)
            return False
        cur = self._s.get(name)
        if cur is None:
            self._s[name] = Status(name, turns, power)
            return True
        cur.turns = max(cur.turns, turns)
        cur.power = max(cur.power, power)
        return False

    def remove(self, name: str) -> None:
        """Remove status ``name`` if present."""
        self._s.pop(name, None)

    def has(self, name: str) -> bool:
        """True if status ``name`` is active."""
        return name in self._s

    def turns(self, name: str) -> int:
        """Turns left on status ``name`` (0 if inactive)."""
        s = self._s.get(name)
        return s.turns if s else 0

    def set_turns(self, name: str, turns: int) -> None:
        """Set the turns left on ``name``, adding it if needed or removing it when ``turns`` <= 0."""
        if turns <= 0:
            self._s.pop(name, None)
        elif name in self._s:
            self._s[name].turns = turns
        else:
            self._s[name] = Status(name, turns)

    def tick(self) -> TickResult:
        """Advance every status by one action: deal damage, then count down."""
        res = TickResult()
        for name in list(self._s):
            st = self._s[name]
            if STATUS_INFO[name][3] and st.power > 0:
                res.damage.append((name, st.power))
            st.turns -= 1
            if st.turns <= 0:
                del self._s[name]
                res.expired.append(name)
        return res

    def speed_multiplier(self) -> float:
        """Speed factor from haste (x2) and slow (x0.5)."""
        m = 1.0
        if "hasted" in self._s:
            m *= 2.0
        if "slowed" in self._s:
            m *= 0.5
        return m

    def labels(self) -> list[tuple[str, str]]:
        """(short label, colour) pairs for the HUD, in a stable order."""
        return [(STATUS_INFO[n][0], STATUS_INFO[n][1]) for n in STATUS_INFO if n in self._s]

    def names(self) -> list[str]:
        """Names of the active statuses, in ``STATUS_INFO`` order."""
        return [n for n in STATUS_INFO if n in self._s]

    def __len__(self) -> int:
        return len(self._s)

    def __contains__(self, name: object) -> bool:
        return name in self._s
