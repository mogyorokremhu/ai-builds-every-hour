"""Phase 53: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase53(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_numbers(self):
        self.check("(sum-between 2 4 '(1 2 3 4 5))", 9)
        self.check("(product-multiples-of 3 '(1 3 6 7))", 18)

    def test_lists(self):
        self.check("(nonuple-all '(1 2))", [9, 18])
        self.check("(evens-cubed '(1 2 3 4))", [8, 64])
        self.check("(odds-cubed '(1 2 3))", [1, 27])
        self.check("(drop-while-even '(2 4 5 6))", [5, 6])
        self.check("(take-while-multiple-of 3 '(3 6 7 9))", [3, 6])
