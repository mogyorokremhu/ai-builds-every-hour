"""Phase 50: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase50(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_numbers(self):
        self.check("(sum-odd-squares '(1 2 3))", 10)
        self.check("(count-multiples-of 3 '(3 4 6 9))", 3)
        self.check("(product-negatives '(-2 3 -4))", 8)

    def test_lists(self):
        self.check("(multiples-of 2 '(1 2 3 4))", [2, 4])
        self.check("(sextuple-all '(1 2))", [6, 12])
        self.check("(list-range-by 0 10 5)", [0, 5, 10])
        self.check("(list-range-by 3 1 1)", [])
        self.check("(take-while-nonzero '(1 2 0 3))", [1, 2])
