"""Melee combat resolution."""
from __future__ import annotations

import random

from .entities import Entity


def attack(attacker: Entity, defender: Entity, rng: random.Random) -> tuple[int, str]:
    """Resolve one melee attack. Returns (damage, message)."""
    assert attacker.fighter and defender.fighter
    roll = rng.randint(-1, 2)
    damage = max(0, attacker.fighter.power + roll - defender.fighter.defense)
    dealt = defender.fighter.take_damage(damage)
    a = "You" if "player" in attacker.tags else f"The {attacker.name}"
    d = "you" if "player" in defender.tags else f"the {defender.name}"
    verb = "hit" if "player" in attacker.tags else "hits"
    if dealt == 0:
        return 0, f"{a} {verb} {d} but deal{'s' if a != 'You' else ''} no damage."
    msg = f"{a} {verb} {d} for {dealt}."
    if not defender.fighter.alive:
        msg += " You die..." if "player" in defender.tags else f" The {defender.name} dies!"
    return dealt, msg
