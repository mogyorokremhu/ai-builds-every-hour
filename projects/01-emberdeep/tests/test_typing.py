"""Final cleanup: typed component accessors, a clean mypy run and full docstring coverage."""
import ast
import subprocess
import sys
import unittest
from pathlib import Path

from emberdeep.entities import Entity, make_monster, make_player
from emberdeep.game import Game
from emberdeep.items import make_item

ROOT = Path(__file__).resolve().parent.parent


class AccessorTest(unittest.TestCase):
    def test_accessors_return_the_components(self):
        p = make_player(1, 1)
        self.assertIs(p.fight, p.fighter)
        self.assertIs(p.pack, p.inventory)
        self.assertIs(p.gear, p.equipment)

    def test_monster_has_fighter_but_no_pack(self):
        m = make_monster("rat", 2, 2)
        self.assertIs(m.fight, m.fighter)
        with self.assertRaises(AttributeError):
            m.gear

    def test_missing_component_raises_attribute_error_naming_the_entity(self):
        e = Entity("pebble", "*", 0, 0)
        for name in ("fight", "pack", "gear", "thing"):
            with self.assertRaisesRegex(AttributeError, "pebble"):
                getattr(e, name)
        # hasattr() keeps working as a "does it have one" test
        self.assertFalse(hasattr(e, "fight"))

    def test_floor_item_thing(self):
        g = Game(seed=3)
        g.place_item(make_item("healing potion"), *g.player.pos)
        ent = g.items_at(*g.player.pos)[0]
        self.assertIs(ent.thing, ent.item)
        self.assertEqual(ent.thing.key, "healing potion")


class CodeQualityTest(unittest.TestCase):
    def test_every_public_definition_has_a_docstring(self):
        missing = []
        for f in sorted((ROOT / "emberdeep").glob("*.py")):
            tree = ast.parse(f.read_text())
            if not ast.get_docstring(tree):
                missing.append(f"{f.name} (module)")
            for n in ast.walk(tree):
                if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and not n.name.startswith("_") \
                        and not ast.get_docstring(n):
                    missing.append(f"{f.name}:{n.lineno} {n.name}")
        self.assertEqual(missing, [])

    def test_mypy_clean(self):
        import importlib.util
        if importlib.util.find_spec("mypy") is None:
            self.skipTest("mypy not installed")
        r = subprocess.run([sys.executable, "-m", "mypy", "emberdeep"], cwd=ROOT,
                           capture_output=True, text=True, timeout=300)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
