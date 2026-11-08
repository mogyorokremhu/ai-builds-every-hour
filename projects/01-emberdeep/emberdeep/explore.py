"""Explore mode (``--explore``): a practice mode that bends the roguelike rules.

* Loading an explore-mode save **keeps** the file, so you can reload after a death
  (the save is only refreshed when you quit).
* Finished explore runs are recorded in the hall of fame as unranked ``[explore]`` entries.
* The wizard menu (``W`` in curses, ``W<letter>`` in text mode) offers debug powers:
  map the level, heal fully, identify everything, jump to the stairs, descend at once
  and summon an item. These only work in explore mode.

Explore mode is part of the run's ``mode`` string, so it survives saving and loading.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from .items import ITEM_TEMPLATES

if TYPE_CHECKING:  # pragma: no cover
    from .game import Game

EXPLORE_MODE = "explore"


def is_explore(mode: str) -> bool:
    return mode == EXPLORE_MODE


def _map(game: "Game") -> str:
    gm = game.gmap
    for y in range(gm.height):
        for x in range(gm.width):
            gm.explored[y][x] = True
    for t in game.traps.values():
        t.hidden = False
    return "The whole level is revealed to you (traps included)."


def _heal(game: "Game") -> str:
    f = game.player.fighter
    f.hp = f.max_hp
    game.player.statuses = type(game.player.statuses)()
    game.resources.torch = max(game.resources.torch, 1400)
    game.resources.food = max(game.resources.food, 1800)
    game.update_fov()
    return "You are fully restored: health, torch and belly."


def _identify(game: "Game") -> str:
    keys = list(game.ident.unknown_kinds())
    for key in keys:
        game.identify_kind(key)
    return f"You know every potion and scroll ({len(keys)} newly identified)."


def _stairs(game: "Game") -> str:
    st = game.gmap.stairs
    if st is None:
        return "There are no stairs on this level."
    blocker = game.blocking_at(*st)
    if blocker is not None and blocker is not game.player:
        return f"The {blocker.name} stands on the stairs."
    game.player.x, game.player.y = st
    game.update_fov()
    return "You blink onto the stairs."


def _descend(game: "Game") -> str:
    if game.gmap.stairs is None:
        return "There is nowhere deeper to go."
    game.player.x, game.player.y = game.gmap.stairs
    game.descend()
    return f"You plunge to depth {game.depth}."


def _summon(game: "Game", key: str = "") -> str:
    key = key or "greater healing potion"
    if key not in ITEM_TEMPLATES:
        return f"No such item: {key}."
    item = game.give(key)
    return f"{item.display_name.capitalize()} appears in your pack."


#: wizard commands: letter -> (description, function)
COMMANDS: dict[str, tuple[str, Callable[["Game"], str]]] = {
    "m": ("map this level", _map),
    "h": ("heal fully (and refuel, feed)", _heal),
    "i": ("identify all potions & scrolls", _identify),
    "s": ("jump to the stairs", _stairs),
    "d": ("descend right now", _descend),
    "g": ("gain a potion of greater healing", _summon),
}


def wizard(game: "Game", letter: str, arg: str = "") -> bool:
    """Run wizard command ``letter``. Returns True if it did anything."""
    if not is_explore(game.mode):
        game.say("Wizard powers only work in explore mode (--explore).")
        return False
    cmd = COMMANDS.get(letter)
    if cmd is None:
        game.say("Unknown wizard command.")
        return False
    text = _summon(game, arg) if letter == "g" and arg else cmd[1](game)
    game.say(f"[wizard] {text}", "bright_magenta")
    return True


def menu_lines() -> list[str]:
    return ["Wizard powers (explore mode)", ""] + [f"{k}) {d}" for k, (d, _) in COMMANDS.items()] + [
        "", "Press a letter, or Esc to cancel."]
