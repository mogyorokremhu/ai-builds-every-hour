"""Regenerate docs/SCREENSHOTS.md: real frames of the curses UI, rendered to text.

Run from the project folder:  python docs/make_screenshots.py

The balance bot plays seeded games; at chosen moments the curses interface draws into an
in-memory screen (the same fake-screen trick the tests use) and the text is captured. So
these "screenshots" are exactly what the game shows in an 80×30 terminal (minus colour).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from emberdeep import effects  # noqa: E402
from emberdeep.bot import Bot  # noqa: E402
from emberdeep.game import Game  # noqa: E402
from emberdeep.render_ascii import render  # noqa: E402
from emberdeep.ui_curses import CursesUI  # noqa: E402

ROWS, COLS = 30, 96


class TextScreen:
    """Minimal curses-window stand-in that records what was drawn."""

    def __init__(self, rows: int = ROWS, cols: int = COLS) -> None:
        self.rows, self.cols = rows, cols
        self.erase()

    def getmaxyx(self) -> tuple[int, int]:
        return self.rows, self.cols

    def erase(self) -> None:
        self.buf = [[" "] * self.cols for _ in range(self.rows)]

    def addstr(self, y: int, x: int, text: str, attr: int = 0) -> None:
        for i, ch in enumerate(text):
            if 0 <= x + i < self.cols:
                self.buf[y][x + i] = ch

    def refresh(self) -> None:
        pass

    def getch(self) -> int:
        return 27

    def text(self) -> str:
        return "\n".join("".join(r).rstrip() for r in self.buf).rstrip("\n")


def frame(game: Game, footer: str = "? for help") -> str:
    scr = TextScreen()
    CursesUI(scr, game).draw(footer=footer)
    return scr.text()


def play_until(game: Game, cond, limit: int = 30000) -> Bot:
    bot = Bot(game)
    n = 0
    while not game.game_over and not cond(game) and n < limit:
        bot.act()
        effects.drain(game)
        n += 1
    return bot


def section(title: str, blurb: str, body: str) -> str:
    return f"## {title}\n\n{blurb}\n\n```text\n{body}\n```\n"


def main() -> None:
    out = ["# Emberdeep — screenshots\n",
           "Real frames from the curses interface (96×30 terminal), captured while the balance bot "
           "plays seeded games. Regenerate with `python docs/make_screenshots.py`.\n"]

    g = Game(42)
    out.append(section("Depth 1 — the Old Cellars", "A fresh run (seed 42). Sidebar: HP, level and XP bars, "
                       "torch and food, equipment, pack fill and what is in view.", frame(g)))

    play_until(g, lambda gm: gm.visible_monsters() and gm.turn > 30)
    out.append(section("First contact", "A few dozen turns later, something has noticed us.", frame(g)))

    g = Game(7)
    play_until(g, lambda gm: gm.depth >= 4 and gm.turn > 10 and gm.visible_monsters())
    out.append(section(f"Depth {g.depth} — {g.theme.name}", "Cellular-automata caves with glowing fungus.",
                       frame(g)))

    g = Game(3)
    play_until(g, lambda gm: gm.depth >= 7 and len(gm.visible_monsters()) >= 1)
    out.append(section(f"Depth {g.depth} — {g.theme.name}", "Lava pools, braziers (`*`) lighting the halls, fire beasts.",
                       frame(g)))

    won = None
    boss_shown = False
    for seed in range(1, 40):
        g = Game(seed)
        play_until(g, lambda gm: gm.depth >= 10 and any("boss" in m.tags for m in gm.visible_monsters()))
        if g.depth >= 10 and not g.game_over:
            if not boss_shown:
                boss_shown = True
                out.append(section("Depth 10 — the Ember Guardian",
                                   "The final arena: the guardian's sanctum inside a ring of lava.", frame(g)))
            play_until(g, lambda gm: False)
            if g.victory:
                won = g
                break
    if won is not None:
        won.conclude()
        scr = TextScreen(rows=40)
        ui = CursesUI(scr, won)
        ui.screen = scr
        ui.timeline_screen("ASCENT — the story of your victory")
        out.append(section("The ascent screen",
                           f"After a win (seed {won.seed}) the run's timeline: depth over time and the notable "
                           "events. `T` shows it at any time; the morgue file has a copy.", scr.text()))

    g = Game(42)
    out.append(section("Text mode", "`python -m emberdeep --text` — the fallback interface for terminals "
                       "without curses.", "\n".join(line.rstrip() for line in render(g).splitlines()).strip("\n")))
    Path(__file__).with_name("SCREENSHOTS.md").write_text("\n".join(out), encoding="utf-8")
    print("wrote docs/SCREENSHOTS.md")


if __name__ == "__main__":
    main()
