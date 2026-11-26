"""Phase 150: list-eighth, list-count-between, list-sum-between, list-product-gt, list-count-even."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase150(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_eighth(self):
        self.check("(list-eighth '(1 2 3 4 5 6 7 8 9))", 8)

    def test_count_between(self):
        self.check("(list-count-between 2 4 '(1 2 3 4 5))", 3)
        self.check("(list-count-between 2 4 '())", 0)

    def test_sum_between(self):
        self.check("(list-sum-between 2 4 '(1 2 3 4 5))", 9)

    def test_product_gt(self):
        self.check("(list-product-gt 2 '(1 3 5 2 4))", 60)
        self.check("(list-product-gt 9 '(1 2))", 1)

    def test_count_even(self):
        self.check("(list-count-even '(1 2 3 4 6))", 3)


if __name__ == "__main__":
    unittest.main()
