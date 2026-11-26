"""Phase 154: list-twelfth, list-count-nonpos, list-sum-nonpos, list-product-odd, list-count-below-mean."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase154(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_twelfth(self):
        self.check("(list-twelfth '(1 2 3 4 5 6 7 8 9 10 11 12 13))", 12)

    def test_count_nonpos(self):
        self.check("(list-count-nonpos '(-1 0 2 -3 4))", 3)

    def test_sum_nonpos(self):
        self.check("(list-sum-nonpos '(-1 0 2 -3 4))", -4)

    def test_product_odd(self):
        self.check("(list-product-odd '(1 2 3 4 5))", 15)
        self.check("(list-product-odd '(2 4))", 1)

    def test_count_below_mean(self):
        self.check("(list-count-below-mean '(1 2 3 4 10))", 3)
        self.check("(list-count-below-mean '())", 0)


if __name__ == "__main__":
    unittest.main()
