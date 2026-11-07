"""Real-time curses interface: scrolling map view, colours, sidebar, log, menus, targeting.

Drawing only goes through a tiny "screen" interface (``getmaxyx``, ``erase``, ``addstr``,
``refresh``, ``getch``), so the whole UI can be driven by a fake screen in tests.
"""
from __future__ import annotations

from typing import Callable, Iterable, Protocol

from . import keys
from .colors import TILE_COLORS, ColorTable
from .game import Game
from .hud import sidebar
from .items import TARGET_CELL, Item
from .look import describe_cell
from .progression import CHOICES
from .targeting import Cursor, blast_area, projectile_path

try:
    import curses
    _CURSES_ERRORS: tuple[type[BaseException], ...] = (curses.error,)
except ImportError:  # pragma: no cover - platform dependent
    curses = None  # type: ignore[assignment]
    _CURSES_ERRORS = ()

SIDEBAR_W = 24
LOG_H = 6


class Screen(Protocol):  # pragma: no cover - typing only
    def getmaxyx(self) -> tuple[int, int]: ...
    def erase(self) -> None: ...
    def addstr(self, y: int, x: int, text: str, attr: int = 0) -> None: ...
    def refresh(self) -> None: ...
    def getch(self) -> int: ...


def camera_offset(target: int, view: int, size: int) -> int:
    """Scroll so ``target`` is centred, clamped to the map edges."""
    if view >= size:
        return 0
    return min(max(target - view // 2, 0), size - view)


class CursesUI:
    def __init__(self, screen: Screen, game: Game, colors: ColorTable | None = None) -> None:
        self.screen = screen
        self.game = game
        self.colors = colors or ColorTable(enabled=False)
        self.running = True

    # ---- low-level drawing ---------------------------------------------
    def size(self) -> tuple[int, int]:
        return self.screen.getmaxyx()

    def put(self, y: int, x: int, text: str, color: str = "white", dim: bool = False,
            reverse: bool = False) -> None:
        rows, cols = self.size()
        if y < 0 or y >= rows or x >= cols or not text:
            return
        if y == rows - 1:  # never write the bottom-right cell (curses raises)
            text = text[: max(0, cols - x - 1)]
        else:
            text = text[: cols - x]
        if not text:
            return
        try:
            self.screen.addstr(y, x, text, self.colors.attr(color, dim, reverse))
        except _CURSES_ERRORS:
            pass

    def layout(self) -> tuple[int, int]:
        rows, cols = self.size()
        view_w = max(10, min(self.game.gmap.width, cols - SIDEBAR_W - 1))
        view_h = max(5, min(self.game.gmap.height, rows - LOG_H - 1))
        return view_w, view_h

    # ---- frame ------------------------------------------------------------
    def draw(self, cursor: Cursor | None = None, item: Item | None = None, footer: str = "",
             show_path: bool = True) -> None:
        g = self.game
        gmap = g.gmap
        self.screen.erase()
        view_w, view_h = self.layout()
        focus = cursor.pos if cursor else g.player.pos
        ox = camera_offset(focus[0], view_w, gmap.width)
        oy = camera_offset(focus[1], view_h, gmap.height)

        for sy in range(view_h):
            my = oy + sy
            if my >= gmap.height:
                break
            for sx in range(view_w):
                mx = ox + sx
                if mx >= gmap.width:
                    break
                tile = gmap.tiles[my][mx]
                lit, remembered = g.theme.tile_colors(tile.name, TILE_COLORS.get(tile.name, ("white", "blue")))
                glyph = tile.glyph
                trap = g.known_trap_at(mx, my)
                if trap is not None:
                    glyph, lit = "^", trap.color
                if gmap.visible[my][mx]:
                    self.put(sy, sx, glyph, lit)
                elif gmap.explored[my][mx]:
                    self.put(sy, sx, glyph, remembered, dim=True)

        def order(e) -> int:
            return 2 if e.is_player else 1 if e.blocks else 0

        for e in sorted(g.entities, key=order):
            sx, sy = e.x - ox, e.y - oy
            if 0 <= sx < view_w and 0 <= sy < view_h and gmap.visible[e.y][e.x]:
                self.put(sy, sx, e.glyph, e.color, dim=e.asleep)

        if cursor is not None:
            overlay: set[tuple[int, int]] = (
                set(projectile_path(gmap, g.player.pos, cursor.pos)) if show_path else set())
            if item is not None and item.radius:
                path = projectile_path(gmap, g.player.pos, cursor.pos)
                center = path[-1] if path else g.player.pos
                overlay |= set(blast_area(gmap, center, item.radius))
            for (x, y) in overlay | {cursor.pos}:
                sx, sy = x - ox, y - oy
                if 0 <= sx < view_w and 0 <= sy < view_h:
                    glyph = self.glyph_at(x, y)
                    color = "bright_yellow" if (x, y) == cursor.pos else "red"
                    self.put(sy, sx, glyph, color, reverse=True)

        # sidebar
        sx0 = view_w + 1
        for i, (text, color) in enumerate(sidebar(g, SIDEBAR_W - 1, max_monsters=max(1, (view_h - 18) // 2))):
            if i >= view_h:
                break
            self.put(i, sx0, text, color)

        # message log
        self.put(view_h, 0, "─" * (view_w + SIDEBAR_W), "blue")
        rows, _ = self.size()
        n = max(1, rows - view_h - 1 - (1 if footer else 0))
        for i, msg in enumerate(g.log.entries(n)):
            self.put(view_h + 1 + i, 0, msg.full_text, msg.color)
        if footer:
            self.put(rows - 1, 0, footer, "bright_white", reverse=True)
        self.screen.refresh()

    def glyph_at(self, x: int, y: int) -> str:
        g = self.game
        for e in sorted(g.entities, key=lambda e: e.blocks, reverse=True):
            if e.pos == (x, y) and g.gmap.visible[y][x]:
                return e.glyph
        if not g.gmap.explored[y][x]:
            return " "
        return "^" if g.known_trap_at(x, y) else g.gmap.tiles[y][x].glyph

    # ---- main loop --------------------------------------------------------
    def run(self) -> None:
        while self.running:
            self.draw(footer="? for help")
            if self.game.game_over:
                self.death_screen()
                return
            if self.game.pending_levels:
                self.level_up()
                continue
            self.handle(self.screen.getch())

    def handle(self, key: int) -> None:
        g = self.game
        if key in keys.MOVE_KEYS:
            g.player_move(*keys.MOVE_KEYS[key])
            return
        if key in keys.WAIT_KEYS:
            g.player_wait()
            return
        cmd = keys.COMMANDS.get(key)
        if cmd == "quit":
            self.running = False
        elif cmd == "pickup":
            g.pickup()
        elif cmd == "descend":
            g.descend()
        elif cmd == "search":
            g.search()
        elif cmd == "pray":
            g.pray()
        elif cmd == "help":
            self.show_text(keys.HELP_TEXT)
        elif cmd == "messages":
            self.message_history()
        elif cmd == "look":
            self.look()
        elif cmd == "inventory":
            item = self.choose_item("Use which item?")
            if item is not None:
                self.use_item(item)
        elif cmd == "drop":
            item = self.choose_item("Drop which item?")
            if item is not None:
                g.drop(item)
        elif cmd == "equip":
            item = self.choose_item("Equip/remove which item?", lambda it: it.is_equipment)
            if item is not None:
                g.toggle_equip(item)

    def use_item(self, item: Item) -> None:
        if item.targeting == TARGET_CELL:
            target = self.target(item)
            if target is None:
                self.game.say("Cancelled.")
                return
            self.game.use(item, target)
        else:
            self.game.use(item)

    # ---- modal screens ----------------------------------------------------
    def choose_item(self, title: str, allowed: Callable[[Item], bool] = lambda it: True) -> Item | None:
        inv = self.game.player.inventory
        eq = self.game.player.equipment
        entries = [(letter, it) for letter, it in inv.listing() if allowed(it)]
        if not entries:
            self.game.say("You have nothing suitable." if len(inv) else "Your pack is empty.")
            return None
        lines: list[tuple[str, str]] = [(title, "bright_white"), ("", "white")]
        for letter, it in entries:
            worn = " (equipped)" if eq.is_equipped(it) else ""
            desc = it.describe()
            lines.append((f"{letter}) {it.glyph} {it.display_name}{worn}" + (f"  — {desc}" if desc else ""),
                          it.color))
        lines += [("", "white"), ("Press a letter, or Esc to cancel.", "white")]
        self.show_box(lines)
        key = self.screen.getch()
        if 0 <= key < 256:
            choice = dict(entries).get(chr(key))
            if choice is not None:
                return choice
        return None

    def target(self, item: Item) -> tuple[int, int] | None:
        """Interactive targeting cursor. Returns the chosen cell or None if cancelled."""
        g = self.game
        foes = [m.pos for m in g.visible_monsters()]
        start = foes[0] if foes else g.player.pos
        cur = Cursor(g.player.pos, start[0], start[1], item.range, g.gmap.width, g.gmap.height)
        while True:
            self.draw(cursor=cur, item=item,
                      footer=f"Aim the {item.name}: move, Tab=next enemy, Enter=fire, Esc=cancel")
            key = self.screen.getch()
            if key in keys.CONFIRM_KEYS:
                return cur.pos
            if key == keys.ESC or key == ord("q") or key == -1:
                return None
            if key == keys.TAB:
                cur.cycle([m.pos for m in g.visible_monsters()])
            elif key in keys.MOVE_KEYS:
                cur.move(*keys.MOVE_KEYS[key])

    def look(self) -> None:
        """Free-moving cursor that describes whatever it rests on. Esc/Enter leaves."""
        g = self.game
        p = g.player.pos
        cur = Cursor(p, p[0], p[1], max(g.gmap.width, g.gmap.height), g.gmap.width, g.gmap.height)
        while True:
            desc = " | ".join(describe_cell(g, *cur.pos))
            self.draw(cursor=cur, footer=f"Look: {desc}  (Esc to leave)", show_path=False)
            key = self.screen.getch()
            if key in keys.MOVE_KEYS:
                cur.move(*keys.MOVE_KEYS[key])
            elif key == keys.TAB:
                cur.cycle([m.pos for m in g.visible_monsters()] + [e.pos for e in g.visible_items()])
            else:
                return

    def show_box(self, lines: Iterable[tuple[str, str]]) -> None:
        lines = list(lines)
        rows, cols = self.size()
        w = min(cols - 2, max(len(t) for t, _ in lines) + 4)
        h = min(rows - 2, len(lines) + 2)
        top, left = max(0, (rows - h) // 2), max(0, (cols - w) // 2)
        self.put(top, left, "┌" + "─" * (w - 2) + "┐", "bright_white")
        for i in range(h - 2):
            text, color = lines[i] if i < len(lines) else ("", "white")
            self.put(top + 1 + i, left, "│ " + " " * (w - 4) + " │", "bright_white")
            self.put(top + 1 + i, left + 2, text[: w - 4], color)
        self.put(top + h - 1, left, "└" + "─" * (w - 2) + "┘", "bright_white")
        self.screen.refresh()

    def show_text(self, text: list[str]) -> None:
        self.screen.erase()
        for i, line in enumerate(text):
            self.put(i, 1, line, "bright_yellow" if i == 0 else "white")
        self.screen.refresh()
        self.screen.getch()

    def message_history(self) -> None:
        msgs = self.game.log.entries()
        offset = 0
        while True:
            rows, _ = self.size()
            page = rows - 2
            self.screen.erase()
            self.put(0, 0, f"Message history ({len(msgs)}) — j/k or PgUp/PgDn to scroll, Esc to leave",
                     "bright_white", reverse=True)
            end = len(msgs) - offset
            for i, msg in enumerate(msgs[max(0, end - page): end]):
                self.put(1 + i, 0, f"[{msg.turn:>5}] {msg.full_text}", msg.color)
            self.screen.refresh()
            key = self.screen.getch()
            max_off = max(0, len(msgs) - page)
            if key in (ord("k"), keys.KEY_UP):
                offset = min(max_off, offset + 1)
            elif key in (ord("j"), keys.KEY_DOWN):
                offset = max(0, offset - 1)
            elif key == keys.KEY_PPAGE:
                offset = min(max_off, offset + page)
            elif key == keys.KEY_NPAGE:
                offset = max(0, offset - page)
            else:
                return

    def level_up(self) -> None:
        """Ask the player to pick a boon for each pending level-up (Esc postpones nothing)."""
        g = self.game
        lines: list[tuple[str, str]] = [
            (f"You reached level {g.level}!", "bright_green"),
            ("", "white"),
        ]
        for key, choice in CHOICES.items():
            lines.append((f"{key}) {choice.label:<9} {choice.description}", "bright_white"))
        lines += [("", "white"), ("Every level also grants +2 max HP.", "white")]
        while g.pending_levels:
            self.draw()
            self.show_box(lines)
            key = self.screen.getch()
            if 0 <= key < 256 and chr(key) in CHOICES:
                g.choose_level_up(chr(key))
            elif key == ord("Q"):
                self.running = False
                return

    def death_screen(self) -> None:
        g = self.game
        self.show_box([
            ("You have perished in Emberdeep.", "bright_red"),
            ("", "white"),
            (f"Cause:         {g.death_cause or 'unknown'}", "white"),
            (f"Depth reached: {g.depth}", "white"),
            (f"Level:         {g.level} ({g.xp} XP)", "white"),
            (f"Kills:         {g.kills}", "white"),
            (f"Turns:         {g.turn}", "white"),
            (f"Seed:          {g.seed}", "white"),
            ("", "white"),
            ("Press any key.", "white"),
        ])
        self.screen.getch()


def play(seed: int | None = None) -> Game:  # pragma: no cover - needs a real terminal
    """Run the curses UI in the current terminal."""
    if curses is None:
        raise RuntimeError("curses is not available on this platform")
    game = Game(seed)

    def _main(stdscr) -> None:
        try:
            curses.curs_set(0)
        except curses.error:
            pass
        stdscr.keypad(True)
        if hasattr(curses, "set_escdelay"):
            curses.set_escdelay(25)
        CursesUI(stdscr, game, ColorTable()).run()

    curses.wrapper(_main)
    return game
