"""Colour names used by the game, and their mapping to curses colour pairs.

Game logic only ever deals in colour *names* ("red", "bright_cyan", ...). The UI turns them
into terminal attributes through :class:`ColorTable`, which degrades gracefully to no colour.
"""
from __future__ import annotations

try:  # curses is missing on stock Windows Python
    import curses
except ImportError:  # pragma: no cover - platform dependent
    curses = None  # type: ignore[assignment]

BASE_COLORS = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")

# Tile colours: (lit, remembered)
TILE_COLORS: dict[str, tuple[str, str]] = {
    "wall": ("yellow", "blue"),
    "floor": ("white", "blue"),
    "door": ("bright_yellow", "blue"),
    "open door": ("yellow", "blue"),
    "stairs down": ("bright_white", "blue"),
    "fungus": ("bright_green", "green"),
    "lava": ("bright_red", "red"),
    "altar": ("bright_magenta", "magenta"),
    "rubble": ("yellow", "blue"),
    "locked door": ("bright_red", "red"),
    "brazier": ("bright_yellow", "yellow"),
}


def split(name: str) -> tuple[str, bool]:
    """'bright_red' -> ('red', True)."""
    if name.startswith("bright_"):
        return name[len("bright_"):], True
    return name, False


class ColorTable:
    """Resolves colour names to curses attributes (or 0 when colour is unavailable)."""

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = bool(enabled and curses is not None)
        self._pairs: dict[str, int] = {}
        if self.enabled:
            try:
                curses.start_color()
                try:
                    curses.use_default_colors()
                    bg = -1
                except curses.error:
                    bg = curses.COLOR_BLACK
                for i, base in enumerate(BASE_COLORS, start=1):
                    curses.init_pair(i, getattr(curses, f"COLOR_{base.upper()}"), bg)
                    self._pairs[base] = i
            except curses.error:
                self.enabled = False

    def attr(self, name: str, dim: bool = False, reverse: bool = False) -> int:
        if curses is None:
            return 0
        base, bright = split(name)
        a = 0
        if self.enabled and base in self._pairs:
            a |= curses.color_pair(self._pairs[base])
        if bright:
            a |= curses.A_BOLD
        if dim:
            a |= curses.A_DIM
        if reverse:
            a |= curses.A_REVERSE
        return a
