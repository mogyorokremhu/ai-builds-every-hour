"""Tests for the curses UI (driven by a fake screen), HUD and text mode."""
import unittest

from emberdeep import keys
from emberdeep.__main__ import run_text_command
from emberdeep.colors import ColorTable, split
from emberdeep.entities import make_monster
from emberdeep.game import Game
from emberdeep.hud import bar, hp_color, sidebar
from emberdeep.items import make_item
from emberdeep.messages import MessageLog
from emberdeep.render_ascii import render, render_inventory
from emberdeep.ui_curses import CursesUI, camera_offset

from tests.helpers import FakeScreen, arena


class HudTests(unittest.TestCase):
    def test_bar(self):
        self.assertEqual(bar(5, 10, 10), "█████░░░░░")
        self.assertEqual(bar(0, 10, 4, "#", "-"), "----")
        self.assertEqual(bar(3, 0, 4), "")

    def test_hp_color(self):
        self.assertEqual(hp_color(10, 10), "bright_green")
        self.assertEqual(hp_color(1, 10), "bright_red")

    def test_sidebar_lists_visible_monsters(self):
        g = arena()
        g.entities.append(make_monster("kobold", g.player.x + 2, g.player.y))
        g.update_fov()
        text = "\n".join(t for t, _ in sidebar(g))
        self.assertIn("kobold", text)
        self.assertIn("HP 30/30", text)
        self.assertTrue(all(len(t) <= 22 for t, _ in sidebar(g)))

    def test_color_split(self):
        self.assertEqual(split("bright_red"), ("red", True))
        self.assertEqual(ColorTable(enabled=False).attr("red"), 0)


class CameraTests(unittest.TestCase):
    def test_camera(self):
        self.assertEqual(camera_offset(5, 40, 70), 0)
        self.assertEqual(camera_offset(69, 40, 70), 30)
        self.assertEqual(camera_offset(35, 40, 70), 15)
        self.assertEqual(camera_offset(10, 80, 70), 0)


class CursesUITests(unittest.TestCase):
    def test_frame_shows_player_sidebar_and_log(self):
        scr = FakeScreen([])
        ui = CursesUI(scr, Game(seed=3))
        ui.draw(footer="? for help")
        text = scr.text()
        self.assertIn("@", text)
        self.assertIn("EMBERDEEP", text)
        self.assertIn("You descend into Emberdeep", text)

    def test_small_terminal_does_not_crash(self):
        for rows, cols in ((12, 40), (24, 80), (50, 200)):
            scr = FakeScreen(["l", "l", "?", "x", "m", 27, "Q"], rows=rows, cols=cols)
            CursesUI(scr, Game(seed=4)).run()
            self.assertGreater(scr.frames, 3)

    def test_movement_keys(self):
        g = arena()
        x, y = g.player.pos
        CursesUI(FakeScreen(["l", keys.KEY_DOWN, "Q"]), g).run()
        self.assertEqual(g.player.pos, (x + 1, y + 1))

    def test_inventory_use_potion(self):
        g = arena()
        g.give("healing potion")
        g.player.fighter.hp = 5
        CursesUI(FakeScreen(["i", "a", "Q"]), g).run()
        self.assertEqual(g.player.fighter.hp, 17)

    def test_pickup_and_equip_via_keys(self):
        g = arena()
        g.place_item(make_item("sword"), *g.player.pos)
        CursesUI(FakeScreen(["g", "w", "a", "Q"]), g).run()
        self.assertTrue(g.player.equipment.is_equipped(g.player.inventory.get("a")))

    def test_targeting_fireball(self):
        g = arena()
        rat = make_monster("rat", g.player.x + 3, g.player.y)
        g.entities.append(rat)
        g.update_fov()
        g.give("fireball scroll")
        CursesUI(FakeScreen(["i", "a", keys.TAB, 10, "Q"]), g).run()
        self.assertFalse(rat.fighter.alive)

    def test_targeting_cancel_keeps_scroll(self):
        g = arena()
        g.give("confusion scroll")
        CursesUI(FakeScreen(["i", "a", "l", keys.ESC, "Q"]), g).run()
        self.assertEqual(len(g.player.inventory), 1)
        self.assertIn("Cancelled.", g.log.last(1))

    def test_drop_via_keys(self):
        g = arena()
        g.give("dagger")
        CursesUI(FakeScreen(["d", "a", "Q"]), g).run()
        self.assertEqual(len(g.player.inventory), 0)
        self.assertEqual(len(g.items_at(*g.player.pos)), 1)

    def test_message_history_scrolls(self):
        g = arena()
        for i in range(80):
            g.say(f"message {i}")
        scr = FakeScreen(["m", "k", "k", keys.KEY_PPAGE, "j", 27, "Q"], rows=20)
        CursesUI(scr, g).run()

    def test_death_screen(self):
        g = arena()
        g.player.fighter.hp = 0
        scr = FakeScreen([ord(" ")])
        CursesUI(scr, g).run()
        self.assertIn("perished", scr.text())


class TextModeTests(unittest.TestCase):
    def test_text_commands(self):
        g = arena()
        g.place_item(make_item("healing potion"), *g.player.pos)
        self.assertTrue(run_text_command(g, "g"))
        self.assertIn("potion of healing", render_inventory(g))
        g.player.fighter.hp = 3
        run_text_command(g, "ua")
        self.assertGreater(g.player.fighter.hp, 3)
        self.assertFalse(run_text_command(g, "dx"))

    def test_render_shows_items(self):
        g = arena()
        g.place_item(make_item("sword"), g.player.x + 1, g.player.y)
        self.assertIn("/", render(g))


class MessageTests(unittest.TestCase):
    def test_entries_keep_color_and_turn(self):
        log = MessageLog()
        log.add("Hot!", "red", 4)
        log.add("Hot!", "red", 5)
        m = log.entries(1)[0]
        self.assertEqual((m.color, m.count, m.turn, m.full_text), ("red", 2, 5, "Hot! (x2)"))
        self.assertEqual(log.last(0), [])


if __name__ == "__main__":
    unittest.main()
