"""Run with:  python -m emberdeep [seed]

Controls (type then Enter): w/a/s/d move, q/e/z/c diagonals, . wait, > descend, x quit.
A real-time curses interface is on the roadmap.
"""
from __future__ import annotations

import sys

from .game import Game
from .render_ascii import render

KEYS = {
    "w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0),
    "q": (-1, -1), "e": (1, -1), "z": (-1, 1), "c": (1, 1),
}


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else None
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
        for ch in cmd or ".":
            if ch == "x":
                return
            if ch in KEYS:
                game.player_move(*KEYS[ch])
            elif ch == ".":
                game.player_wait()
            elif ch == ">":
                game.descend()


if __name__ == "__main__":
    main()
