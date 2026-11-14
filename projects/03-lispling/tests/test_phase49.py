"""Phase 49: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase49(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_numbers(self):
        self.check("(sum-negatives '(-1 2 -3))", -4)
        self.check("(product-positives '(-1 2 3))", 6)
        self.check("(count-nonzero '(0 1 0 2))", 2)

    def test_lists(self):
        self.check("(drop-while-negative '(-1 -2 3 -4))", [3, -4])
        self.check("(quintuple-all '(1 2 3))", [5, 10, 15])
        self.check("(nonzeros '(0 1 0 2))", [1, 2])
        self.check("(list-range-step-up 2 5)", [2, 3, 4, 5])
        self.check("(list-range-step-up 5 2)", [])
