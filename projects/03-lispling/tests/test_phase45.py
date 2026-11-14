"""Phase 45: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase45(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_counts(self):
        self.check("(count-evens '(1 2 3 4))", 2)
        self.check("(count-odds '(1 2 3 4 5))", 3)
        self.check("(sum-evens '(1 2 3 4))", 6)

    def test_lists(self):
        self.check("(repeat-list '(1 2) 3)", [1, 2, 1, 2, 1, 2])
        self.check("(repeat-list '(1) 0)", [])
        self.check("(negate-all '(1 -2 3))", [-1, 2, -3])
        self.check("(alternate '(1 3 5) '(2 4))", [1, 2, 3, 4, 5])

    def test_cube(self):
        self.check("(cube 3)", 27)
