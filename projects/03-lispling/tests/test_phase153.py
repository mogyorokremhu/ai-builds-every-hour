"""Phase 153: list-eleventh, list-count-nonneg, list-sum-nonneg, list-product-even, list-count-above-mean."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase153(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_eleventh(self):
        self.check("(list-eleventh '(1 2 3 4 5 6 7 8 9 10 11 12))", 11)

    def test_count_nonneg(self):
        self.check("(list-count-nonneg '(-1 0 2 -3 4))", 3)

    def test_sum_nonneg(self):
        self.check("(list-sum-nonneg '(-1 0 2 -3 4))", 6)

    def test_product_even(self):
        self.check("(list-product-even '(1 2 3 4 5))", 8)
        self.check("(list-product-even '(1 3))", 1)

    def test_count_above_mean(self):
        self.check("(list-count-above-mean '(1 2 3 4 10))", 1)
        self.check("(list-count-above-mean '())", 0)


if __name__ == "__main__":
    unittest.main()
