"""Run with:  python -m emberdeep [seed] [--text]

Uses the real-time curses interface when available (Linux/macOS terminals), otherwise
falls back to the line-based text mode. Pass ``--text`` to force text mode.

Text-mode controls (type then Enter, chainable): w/a/s/d move, q/e/z/c diagonals,
. wait, g pick up, i inventory, u<letter> use/equip, r<letter> drop, > descend, x quit.
"""
from __future__ import annotations

import sys

from .game import Game
from .render_ascii import render, render_inventory

KEYS = {
    "w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0),
    "q": (-1, -1), "e": (1, -1), "z": (-1, 1), "c": (1, 1),
}


def run_text_command(game: Game, cmd: str) -> bool:
    """Execute a chain of text-mode commands. Returns False if the player quit."""
    chars = iter(cmd or ".")
    for ch in chars:
        if ch == "x":
            return False
        if ch in KEYS:
            game.player_move(*KEYS[ch])
        elif ch == ".":
            game.player_wait()
        elif ch == ">":
            game.descend()
        elif ch == "g":
            game.pickup()
        elif ch == "i":
            print(render_inventory(game))
        elif ch in "ur":
            letter = next(chars, "")
            item = game.player.inventory.get(letter)
            if item is None:
                game.say("No such item.")
            elif ch == "r":
                game.drop(item)
            elif item.targeting == "cell":
                foes = game.visible_monsters()
                if foes:
                    game.use(item, foes[0].pos)
                else:
                    game.say("No target in view.")
            else:
                game.use(item)
        if game.game_over:
            break
    return True


def text_main(seed: int | None) -> None:
    game = Game(seed)
    while True:
        print("\n" * 2 + render(game))
        if game.game_over:
            print(f"\nYou died on depth {game.depth} with {game.xp} XP.")
            return
        try:
            cmd = input("> ").strip().lower()
        except EOFError:
            return
        if not run_text_command(game, cmd):
            return


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    force_text = "--text" in args
    args = [a for a in args if a != "--text"]
    seed = int(args[0]) if args else None
    if not force_text and sys.stdout.isatty():
        try:
            from .ui_curses import play

            play(seed)
            return
        except (ImportError, RuntimeError):
            pass
    text_main(seed)


if __name__ == "__main__":
    main()
