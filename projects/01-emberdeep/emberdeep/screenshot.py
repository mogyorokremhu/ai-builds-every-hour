"""ASCII screenshots of the real curses UI, for the docs (``python -m emberdeep.screenshot``).

The curses front-end only talks to a tiny screen interface, so we can point it at an
in-memory :class:`TextScreen` and read back exactly what a terminal would show. The
balance bot plays a seeded game for a while to get somewhere interesting first.

    python -m emberdeep.screenshot                 # writes SCREENSHOTS.md
    python -m emberdeep.screenshot out.md 7 900    # seed 7, 900 bot actions
"""
from __future__ import annotations

import sys

from .bot import Bot
from .game import Game
from .ui_curses import CursesUI


class TextScreen:
    """A minimal in-memory stand-in for a curses window."""

    def __init__(self, rows: int = 30, cols: int = 96) -> None:
        self.rows, self.cols = rows, cols
        self.erase()

    def getmaxyx(self) -> tuple[int, int]:
        """The fake screen's (rows, cols)."""
        return self.rows, self.cols

    def erase(self) -> None:
        """Blank the buffer."""
        self.buf = [[" "] * self.cols for _ in range(self.rows)]

    def addstr(self, y: int, x: int, text: str, attr: int = 0) -> None:
        """Write ``text`` into the buffer at (y, x), clipping at the edges."""
        for i, ch in enumerate(text):
            if 0 <= y < self.rows and 0 <= x + i < self.cols:
                self.buf[y][x + i] = ch

    def refresh(self) -> None:
        """No-op: nothing to flush."""
        pass

    def getch(self) -> int:
        """Always return Esc, so any prompt is dismissed."""
        return 27

    def text(self) -> str:
        """The buffer as text, with trailing spaces trimmed."""
        return "\n".join("".join(r).rstrip() for r in self.buf)


def advance(game: Game, actions: int) -> Game:
    """Let the bot play ``actions`` moves (stopping early if the run ends)."""
    bot = Bot(game)
    for _ in range(actions):
        if game.game_over:
            break
        bot.act()
    while game.pending_levels:
        game.choose_level_up("m")
    return game


def capture(game: Game, rows: int = 30, cols: int = 96, view: str = "map") -> str:
    """Render one screen of ``game``: ``map``, ``help``, ``timeline`` or ``inventory``."""
    scr = TextScreen(rows, cols)
    ui = CursesUI(scr, game)
    if view == "map":
        ui.draw(footer="? for help")
    elif view == "timeline":
        ui.screen.erase()
        for i, line in enumerate(ui.timeline_lines(final=game.game_over)):
            ui.put(i, 1, line)
    elif view == "inventory":
        ui.draw()
        ui.choose_item("Use which item?")
    elif view == "help":
        from .keys import HELP_TEXT

        for i, line in enumerate(HELP_TEXT[:rows]):
            ui.put(i, 1, line)
    else:
        raise ValueError(view)
    return scr.text()


def document(seed: int = 7, actions: int = 900) -> str:
    """Build the Markdown screenshots document from a bot-played game of ``seed``."""
    g = advance(Game(seed), actions)
    shots = [
        ("Exploring", "The map, the sidebar (HP, XP, torch, food, load, gear, monsters in view) and the "
                      "message log.", capture(g)),
        ("Inventory", "Letters a–z; unidentified potions and scrolls show their random appearance.",
         capture(g, view="inventory")),
        ("Run timeline (`T`)", "Depth over time plus notable events — also shown after every run.",
         capture(g, rows=24, view="timeline")),
    ]
    out = ["# Emberdeep screenshots", "",
           f"Captured from the real curses UI with `python -m emberdeep.screenshot` "
           f"(seed {seed}, after {actions} balance-bot actions; colours not shown).", ""]
    for title, caption, text in shots:
        out += [f"## {title}", "", caption, "", "```", text.rstrip("\n"), "```", ""]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> None:  # pragma: no cover - CLI
    """CLI: write the screenshots document to a file (default ``SCREENSHOTS.md``)."""
    args = list(sys.argv[1:] if argv is None else argv)
    path = args[0] if args else "SCREENSHOTS.md"
    seed = int(args[1]) if len(args) > 1 else 7
    actions = int(args[2]) if len(args) > 2 else 900
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(document(seed, actions))
    print(f"wrote {path}")


if __name__ == "__main__":  # pragma: no cover
    main()
