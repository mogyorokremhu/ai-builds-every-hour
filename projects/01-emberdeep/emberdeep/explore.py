"""Explore ("wizard") mode: a forgiving way to learn the dungeon.

Start it with ``python -m emberdeep --explore``. An explore run

* keeps its save when loaded (no permadeath: reload as often as you like);
* rescues you from death — you wake up at full health where you fell, and the death is
  noted in the timeline and the morgue file;
* is never ranked in the hall of fame (it is listed as ``[explore]``).

Rescue happens the moment the game notices the player died (see
:meth:`emberdeep.game.Game.game_over`), uses no randomness and so keeps replays
deterministic.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .game import Game

MODE = "explore"
REVIVE_FOOD = 400   # food restored if you starved


def is_explore(mode: str) -> bool:
    return mode == MODE


def revive(game: "Game") -> bool:
    """If this is an explore run and the player is dead, bring them back. Returns True if so."""
    p = game.player
    if not is_explore(game.mode) or p.fighter is None or p.fighter.alive:
        return False
    cause = game.death_cause or "died"
    game.explore_deaths.append(cause)
    p.fighter.hp = p.fighter.max_hp
    p.statuses = type(p.statuses)()
    if game.resources.food < REVIVE_FOOD:
        game.resources.food = REVIVE_FOOD
        game.resources._turns_starving = 0
    game.death_cause = None
    game.timeline.add(game.turn, game.depth, "revive", f"Rescued from death ({cause})")
    game.say(f"You would have died ({cause}), but the deep is merciful in explore mode.", "bright_cyan")
    return True
