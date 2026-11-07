"""Run with:  python -m emberdeep [seed] [--text] [--daily[=YYYY-MM-DD]] [--new] [--scores]

Uses the real-time curses interface when available (Linux/macOS terminals), otherwise
falls back to the line-based text mode. Pass ``--text`` to force text mode.

* A saved game is resumed automatically (and the save deleted: permadeath). ``--new``
  ignores it; quitting saves again.
* ``--daily`` plays today's shared dungeon; ``--daily=2026-11-07`` replays a past day.
* ``--scores`` prints the hall of fame and exits.
* Files live in ``$EMBERDEEP_HOME`` (default ``~/.emberdeep``).

Text-mode controls (type then Enter, chainable): w/a/s/d move, q/e/z/c diagonals,
. wait, g pick up, i inventory, u<letter> use/equip, r<letter> drop, > descend,
x save & quit, f search for traps, p pray at an altar, k close an adjacent door,
+v/+m/+g choose a level-up boon. Bump into a closed door (+) to open it.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from . import daily, save, scores
from .game import Game
from .morgue import finish_run
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
        elif ch == "f":
            game.search()
        elif ch == "p":
            game.pray()
        elif ch == "k":
            doors = game.closable_doors()
            if doors:
                px, py = game.player.pos
                game.close_door(doors[0][0] - px, doors[0][1] - py)
            else:
                game.say("There is no open door next to you.")
        elif ch == "+":
            if not game.choose_level_up(next(chars, "")):
                game.say("Use +v, +m or +g when you have a level-up.")
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


@dataclass
class Options:
    seed: int | None = None
    text: bool = False
    daily: str | None = None   # ISO date, or "" for today
    new: bool = False
    scores: bool = False


def parse_args(argv: list[str]) -> Options:
    opts = Options()
    for a in argv:
        if a == "--text":
            opts.text = True
        elif a == "--new":
            opts.new = True
        elif a == "--scores":
            opts.scores = True
        elif a == "--daily":
            opts.daily = ""
        elif a.startswith("--daily="):
            opts.daily = a.split("=", 1)[1]
        elif a.lstrip("-").isdigit():
            opts.seed = int(a)
        else:
            raise SystemExit(f"unknown argument: {a}\n\n{__doc__}")
    return opts


def start_game(opts: Options, home: Path) -> Game:
    """Resume the saved run when appropriate, otherwise start a new one."""
    path = save.save_path(home)
    if opts.daily is not None:
        day = daily.parse_date(opts.daily) if opts.daily else daily.today()
        game = Game(daily.daily_seed(day), mode=daily.daily_mode(day))
        game.say(f"Daily run for {day.isoformat()}: everyone gets this dungeon today.", "bright_cyan")
        return game
    if opts.seed is None and not opts.new and save.has_save(path):
        try:
            return save.load_game(path)
        except save.SaveError as exc:
            print(f"Could not load the saved game ({exc}); starting a new one.")
            save.delete_save(path)
    return Game(opts.seed)


def end_session(game: Game, home: Path, recorded: bool) -> list[str]:
    """After the UI exits: record a finished run, or save a live one. Returns report lines."""
    if game.game_over:
        if recorded:
            return []
        return finish_run(game, home).lines()
    path = save.save_game(game, save.save_path(home))
    return [f"Game saved to {path}. Run again to continue."]


def text_main(game: Game, home: Path) -> list[str]:
    while True:
        print("\n" * 2 + render(game))
        if game.game_over:
            if game.victory:
                print(f"\nVICTORY! You carried off the Ember Heart in {game.turn} turns.")
            else:
                print(f"\nYou died on depth {game.depth} at level {game.level} ({game.xp} XP): "
                      f"{game.death_cause or 'unknown'}.")
            return end_session(game, home, recorded=False)
        try:
            cmd = input("> ").strip().lower()
        except EOFError:
            return end_session(game, home, recorded=False)
        if not run_text_command(game, cmd):
            return end_session(game, home, recorded=False)


def main(argv: list[str] | None = None) -> None:
    opts = parse_args(list(sys.argv[1:] if argv is None else argv))
    home = save.data_dir()
    if opts.scores:
        print("\n".join(["EMBERDEEP — hall of fame", ""] + scores.format_table(scores.load_scores(home), 20)))
        return
    game = start_game(opts, home)
    report: list[str]
    if not opts.text and sys.stdout.isatty():
        try:
            from .ui_curses import play

            recorded: list[bool] = []

            def on_finish(g: Game) -> list[str]:
                recorded.append(True)
                return finish_run(g, home).lines()

            play(game, on_finish=on_finish, home=home)
            report = end_session(game, home, recorded=bool(recorded))
            print("\n".join(report))
            return
        except (ImportError, RuntimeError):
            pass
    report = text_main(game, home)
    print("\n".join(report))


if __name__ == "__main__":
    main()
