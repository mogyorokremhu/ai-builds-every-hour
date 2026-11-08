"""Knockback: heavy blows shove creatures back a square — sometimes into lava.

* The **warhammer** has a chance to knock its target back on every hit.
* **Cave trolls** can hurl *you* back with their blows.

A creature knocked into lava is consumed — unless it is a fire creature (immune to burning),
which simply climbs back out. The player is never pushed *into* lava, but is badly scorched
at its edge. The boss is too heavy to move. Walls, closed doors and other creatures stop a
shove.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .entities import Entity
    from .game import Game

LAVA_EDGE_DAMAGE = 8
LAVA_EDGE_BURN = 4
TROLL_SHOVE_CHANCE = 0.25


def _sign(v: int) -> int:
    return (v > 0) - (v < 0)


def shove(game: "Game", attacker: "Entity", target: "Entity") -> str:
    """Push ``target`` one cell directly away from ``attacker``.

    Returns what happened: ``"moved"``, ``"lava"`` (consumed by lava), ``"scorched"``
    (the player at the lava's edge), ``"climbed"`` (fire creature), ``"blocked"`` or
    ``"immovable"``.
    """
    from .game import C_BAD, C_GOOD

    if "boss" in target.tags:
        return "immovable"
    dx, dy = _sign(target.x - attacker.x), _sign(target.y - attacker.y)
    if (dx, dy) == (0, 0):
        return "blocked"
    nx, ny = target.x + dx, target.y + dy
    tile = game.gmap.get(nx, ny)
    seen = game.gmap.visible[target.y][target.x]
    if game.blocking_at(nx, ny) is not None:
        return "blocked"
    if tile.name == "lava":
        if target.is_player:
            dealt = target.fighter.take_damage(LAVA_EDGE_DAMAGE)
            game.say(f"You are hurled to the lava's edge and scorched for {dealt}!", C_BAD)
            if not target.fighter.alive:
                game.death_cause = "hurled into lava"
                game.say("You die...", C_BAD)
                return "scorched"
            game.apply_status(target, "burning", LAVA_EDGE_BURN, 2)
            return "scorched"
        if target.immune_to("burning"):
            if seen:
                game.say(f"The {target.name} splashes into the lava and climbs right back out.")
            return "climbed"
        if seen:
            game.say(f"The {target.name} is knocked into the lava and consumed!", C_GOOD)
        target.fighter.hp = 0
        game.on_kill(target)
        if target in game.entities:  # nothing is left to leave a corpse
            game.entities.remove(target)
        return "lava"
    if not tile.walkable:
        return "blocked"
    target.move(dx, dy)
    if target.is_player:
        game.say("The blow knocks you back!", C_BAD)
        game.update_fov()
    elif seen:
        game.say(f"The {target.name} is knocked back!")
    return "moved"
