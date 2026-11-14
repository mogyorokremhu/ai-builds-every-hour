"""Phase 51: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase51(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_numbers(self):
        self.check("(sum-even-squares '(1 2 3 4))", 20)
        self.check("(product-odds '(1 2 3 5))", 15)
        self.check("(count-between 2 4 '(1 2 3 4 5))", 3)

    def test_lists(self):
        self.check("(evens-squared '(1 2 3 4))", [4, 16])
        self.check("(septuple-all '(1 2))", [7, 14])
        self.check("(take-while-even '(2 4 5 6))", [2, 4])
        self.check("(drop-while-nonzero '(1 2 0 3))", [0, 3])
