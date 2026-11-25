"""Phase 139: list-take-while, list-drop-while, list-frequencies, list-mode, list-find-index."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase139(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_take_while(self):
        self.check("(list-take-while even? '(2 4 5 6))", [2, 4])
        self.check("(list-take-while even? '())", [])

    def test_drop_while(self):
        self.check("(list-drop-while even? '(2 4 5 6))", [5, 6])
        self.check("(list-drop-while even? '(2 4))", [])

    def test_frequencies(self):
        self.check("(map cdr (list-frequencies '(1 2 1 3 1 2)))", [3, 2, 1])
        self.check("(map car (list-frequencies '(1 2 1 3 1 2)))", [1, 2, 3])

    def test_mode(self):
        self.check("(list-mode '(1 2 2 3 3 3))", 3)
        self.check("(list-mode '(5 5 7 7))", 5)

    def test_find_index(self):
        self.check("(list-find-index even? '(1 3 4 5))", 2)
        self.check("(list-find-index even? '(1 3))", -1)


if __name__ == "__main__":
    unittest.main()
