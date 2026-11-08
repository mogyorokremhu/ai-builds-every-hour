"""Throwing items (``t``): daggers fly true, potions shatter on impact.

The item travels along the targeting line and stops at the first creature in its way (or
the target cell, or a wall). What happens depends on what you threw:

* **potions** shatter. Liquid fire bursts into flame around the impact, venom leaves a
  poisonous splash, healing/speed potions affect whatever they hit. Shattering a potion
  identifies it.
* **weapons** deal damage (daggers are made for it) and land at the target's feet.
* anything else lands where it stops, bonking a creature for 1 if it hits one.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from . import fx
from .geometry import chebyshev
from .targeting import blast_area, projectile_path

if TYPE_CHECKING:  # pragma: no cover
    from .entities import Entity
    from .game import Game
    from .items import Item

THROW_RANGE = 7


def flight(game: "Game", target: tuple[int, int]) -> tuple[list[tuple[int, int]], "Entity | None"]:
    """Cells the thrown item crosses and the creature it hits first (if any)."""
    path = projectile_path(game.gmap, game.player.pos, target)
    for i, cell in enumerate(path):
        m = game.monster_at(*cell)
        if m is not None:
            return path[: i + 1], m
    return path, None


def can_throw(game: "Game", item: "Item", target: tuple[int, int]) -> str | None:
    """Why ``item`` can't be thrown at ``target`` (None if it can)."""
    if item.kind == "artifact":
        return "You won't let go of that."
    gm = game.gmap
    if not gm.in_bounds(*target) or not gm.visible[target[1]][target[0]]:
        return "You can't see that spot."
    if chebyshev(target, game.player.pos) > THROW_RANGE:
        return "That is too far to throw."
    if target == game.player.pos:
        return "You toss it from hand to hand."
    if not projectile_path(gm, game.player.pos, target):
        return "There is no room to throw."
    return None


def throw(game: "Game", item: "Item", target: tuple[int, int]) -> bool:
    """Throw one ``item`` from the pack at ``target``. Returns True if a turn was spent."""
    from .game import C_BAD, C_INFO, C_MAGIC, NOISE

    reason = can_throw(game, item, target)
    if reason is not None:
        game.say(reason)
        return False
    player = game.player
    eq = player.gear
    if eq.is_equipped(item) and item.count <= 1:
        eq.unequip(item)
        eq.apply_to(player.fight)
    shown = item.shown_name
    one = player.pack.take_one(item)
    path, victim = flight(game, target)
    land = path[-1]
    fx.emit(game, "bolt", path, one.glyph, one.color)
    game.noise = NOISE["item"]
    if one.kind == "potion":
        game.say(f"The {shown} shatters!", C_MAGIC)
        _shatter(game, one, land, victim)
        if game.identify_kind(one.key):
            game.say(f"(That was {one.name}.)", C_MAGIC)
        return True
    if victim is not None:
        if one.is_equipment and one.slot == "weapon":
            raw = 2 + one.power_bonus + one.thrown_damage + game.rng.randint(0, 2)
            dmg = max(1, raw - victim.fight.defense)
        else:
            dmg = 1
        game.say(f"The {shown} hits the {victim.name}.", C_INFO)
        game.damage_monster(victim, dmg, "hit")
    elif game.gmap.visible[land[1]][land[0]]:
        game.say(f"The {shown} clatters to the floor.")
    game.place_item(one, *land)
    if not player.fight.alive:  # pragma: no cover - defensive
        game.say("You die...", C_BAD)
    return True


def _shatter(game: "Game", potion: "Item", at: tuple[int, int], victim: "Entity | None") -> None:
    from .game import C_BAD

    effect = potion.effect
    if effect in ("firebomb", "venom"):
        area = blast_area(game.gmap, at, potion.radius)
        fx.emit(game, "blast", [at] + [c for c in area if c != at], "*",
                "bright_red" if effect == "firebomb" else "bright_green")
        for cell in area:
            who = game.player if cell == game.player.pos else game.monster_at(*cell)
            if who is None:
                continue
            if effect == "firebomb":
                if who.is_player:
                    dealt = who.fight.take_damage(potion.magnitude // 2)
                    game.say(f"The flames lick you for {dealt}!", C_BAD)
                    if not who.fight.alive:
                        game.death_cause = "burned by liquid fire"
                        game.say("You die...", C_BAD)
                        return
                    game.apply_status(who, "burning", 3, 1)
                elif who.immune_to("burning"):
                    game.say(f"The {who.name} basks in the flames.")
                else:
                    game.damage_monster(who, potion.magnitude, "engulfed in flame")
                    if who.fight.alive:
                        game.apply_status(who, "burning", 3, 2)
            else:
                game.apply_status(who, "poisoned", potion.magnitude, 2)
        return
    if victim is None:
        game.say("The liquid splashes harmlessly.")
        return
    if effect == "heal":
        healed = victim.fight.heal(potion.magnitude)
        game.say(f"The {victim.name} looks healthier (+{healed}).")
    elif effect == "haste":
        game.apply_status(victim, "hasted", potion.magnitude)
    else:  # pragma: no cover - every potion effect is covered above
        game.say("The liquid splashes harmlessly.")
