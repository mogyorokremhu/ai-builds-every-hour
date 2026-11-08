"""Command line, text mode and documentation helpers."""
import builtins
import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from emberdeep import __main__ as cli
from emberdeep import save, screenshot, throwing
from emberdeep.game import Game
from emberdeep.items import make_item

from tests.helpers import arena


class CliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.home = Path(self._tmp.name)
        self._env = mock.patch.dict(os.environ, {"EMBERDEEP_HOME": str(self.home)})
        self._env.start()

    def tearDown(self):
        self._env.stop()
        self._tmp.cleanup()

    def run_main(self, argv, inputs):
        feed = iter(inputs)

        def fake_input(prompt=""):
            try:
                return next(feed)
            except StopIteration:
                raise EOFError from None

        out = io.StringIO()
        with mock.patch.object(builtins, "input", fake_input), contextlib.redirect_stdout(out):
            cli.main(argv)
        return out.getvalue()

    def test_unknown_argument(self):
        with self.assertRaises(SystemExit):
            cli.parse_args(["--bogus"])

    def test_scores_flag(self):
        text = self.run_main(["--scores"], [])
        self.assertIn("hall of fame", text)

    def test_text_mode_saves_on_quit_and_resumes(self):
        text = self.run_main(["--text", "--new", "5"], ["dd", "i", "x"])
        self.assertIn("Game saved", text)
        self.assertTrue(save.has_save(save.save_path(self.home)))
        text = self.run_main(["--text"], ["T", "x"])
        self.assertIn("Welcome back", text)
        self.assertIn("Turns per depth", text)

    def test_text_mode_eof_saves(self):
        text = self.run_main(["--text", "--new"], [])
        self.assertIn("Game saved", text)

    def test_text_mode_death_records_run(self):
        real = cli.run_text_command

        def kill(game, cmd):
            result = real(game, ".")
            game.player.fighter.hp = 0
            game.death_cause = "killed by a test"
            return result

        with mock.patch.object(cli, "run_text_command", kill):
            text = self.run_main(["--text", "--new", "3"], ["."])
        self.assertIn("You died", text)
        self.assertIn("Morgue file", text)
        self.assertFalse(save.has_save(save.save_path(self.home)))

    def test_corrupt_save_starts_new(self):
        save.save_path(self.home).write_text("{not json", encoding="utf-8")
        text = self.run_main(["--text"], ["x"])
        self.assertIn("Could not load", text)

    def test_text_commands(self):
        g = arena()
        g.give("healing potion")
        cli.run_text_command(g, "uz")      # no such item
        cli.run_text_command(g, "rz")
        cli.run_text_command(g, "tz")
        cli.run_text_command(g, "ta")      # nothing to throw at
        cli.run_text_command(g, "+x")      # no level-up pending
        cli.run_text_command(g, "k")       # no door
        cli.run_text_command(g, "fpg>")    # search, pray, pick up, descend (all harmless here)
        text = "\n".join(m.text for m in g.log.entries())
        self.assertIn("No such item", text)
        self.assertIn("No target in view", text)
        self.assertIn("level-up", text)
        self.assertFalse(cli.run_text_command(g, "x"))
        scroll = g.give("fireball scroll")
        scroll.unknown_name = None
        cli.run_text_command(g, "u" + g.player.inventory.letter_of(scroll))
        self.assertIn("No target in view", g.log.entries()[-1].text)


class ScreenshotTests(unittest.TestCase):
    def test_capture_views(self):
        g = screenshot.advance(Game(7), 60)
        for view in ("map", "inventory", "timeline", "help"):
            text = screenshot.capture(g, view=view)
            self.assertTrue(text.strip())
        self.assertIn("EMBERDEEP", screenshot.capture(g))
        with self.assertRaises(ValueError):
            screenshot.capture(g, view="nope")

    def test_document(self):
        doc = screenshot.document(seed=3, actions=40)
        self.assertIn("# Emberdeep screenshots", doc)
        self.assertEqual(doc.count("```"), 6)


class ThrowEdgeTests(unittest.TestCase):
    def test_cannot_throw_artifact_or_out_of_range(self):
        g = arena(w=30)
        heart = make_item("ember heart")
        self.assertIn("won't let go", throwing.can_throw(g, heart, (g.player.x + 1, g.player.y)))
        dagger = make_item("dagger")
        g.gmap.visible[g.player.y][g.player.x + 8] = True
        self.assertIn("too far", throwing.can_throw(g, dagger, (g.player.x + 8, g.player.y)))
        self.assertIn("hand to hand", throwing.can_throw(g, dagger, g.player.pos))

    def test_potion_splashes_on_floor_and_hits_monster(self):
        from emberdeep.entities import make_monster

        g = arena()
        heal = g.give("healing potion")
        g.throw(heal, (g.player.x + 3, g.player.y))
        self.assertTrue(any("harmlessly" in m.text for m in g.log.entries()))
        rat = make_monster("rat", g.player.x + 2, g.player.y)
        rat.fighter.hp = 1
        g.entities.append(rat)
        g.update_fov()
        speed = g.give("speed potion")
        g.throw(speed, rat.pos)
        self.assertTrue(rat.statuses.has("hasted"))
        heal = g.give("healing potion")
        g.throw(heal, rat.pos)
        self.assertGreater(rat.fighter.hp, 1)


if __name__ == "__main__":
    unittest.main()
