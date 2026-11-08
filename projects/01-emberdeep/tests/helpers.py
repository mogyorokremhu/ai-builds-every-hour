"""Shared test helpers: a fake curses screen and a tiny hand-built arena."""
from __future__ import annotations

from emberdeep.game import Game
from emberdeep.gamemap import GameMap
from emberdeep.tiles import FLOOR, WALL


class FakeScreen:
    """Implements the subset of the curses window API the UI uses, with scripted keys."""

    def __init__(self, keys: list[int | str], rows: int = 30, cols: int = 100) -> None:
        self.rows, self.cols = rows, cols
        self.keys = [ord(k) if isinstance(k, str) else k for k in keys]
        self.erase()
        self.frames = 0
        self.snapshots: list[str] = []  # screen text each time a key was read

    def getmaxyx(self) -> tuple[int, int]:
        return self.rows, self.cols

    def erase(self) -> None:
        self.buf = [[" "] * self.cols for _ in range(self.rows)]

    def addstr(self, y: int, x: int, text: str, attr: int = 0) -> None:
        if not (0 <= y < self.rows) or x < 0 or x + len(text) > self.cols:
            raise AssertionError(f"write out of bounds at {y},{x}: {text!r}")
        if y == self.rows - 1 and x + len(text) >= self.cols:
            raise AssertionError("wrote bottom-right cell")
        for i, ch in enumerate(text):
            self.buf[y][x + i] = ch

    def refresh(self) -> None:
        self.frames += 1

    def getch(self) -> int:
        self.snapshots.append(self.text())
        return self.keys.pop(0) if self.keys else ord("Q")

    def seen(self, text: str) -> bool:
        """True if ``text`` was on screen at any key prompt (or is on it now)."""
        return any(text in snap for snap in self.snapshots) or text in self.text()

    def text(self) -> str:
        return "\n".join("".join(r) for r in self.buf)


def arena(seed: int = 1, w: int = 20, h: int = 12) -> Game:
    """A Game whose level is one open room with the player in the middle and no monsters."""
    g = Game(seed)
    gm = GameMap(w, h)
    for y in range(h):
        for x in range(w):
            gm.set(x, y, WALL if x in (0, w - 1) or y in (0, h - 1) else FLOOR)
    g.gmap = gm
    g.player.x, g.player.y = w // 2, h // 2
    g.entities = [g.player]
    g.update_fov()
    return g
