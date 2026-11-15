"""Phase 55: statistics helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase55(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_range_variance(self):
        self.check("(range-of '(3 9 4))", 6)
        self.check("(variance '(2 4 4 4 5 5 7 9))", 4)
        self.check("(mean-absolute-deviation '(2 4 4 4 5 5 7 9))", 1.5)

    def test_cumulative_product(self):
        self.check("(cumulative-product '(1 2 3 4))", [1, 2, 6, 24])
