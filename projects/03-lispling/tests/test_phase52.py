"""Phase 52: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase52(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_numbers(self):
        self.check("(sum-multiples-of 3 '(1 3 6 7 9))", 18)
        self.check("(count-less-than 3 '(1 2 3 4))", 2)
        self.check("(count-greater-than 3 '(1 2 3 4 5))", 2)

    def test_lists(self):
        self.check("(octuple-all '(1 2))", [8, 16])
        self.check("(take-while-odd '(1 3 4 5))", [1, 3])
        self.check("(drop-while-odd '(1 3 4 5))", [4, 5])
        self.check("(odds-squared '(1 2 3))", [1, 9])
