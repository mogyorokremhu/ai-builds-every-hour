"""Phase 159: list-seventeenth, list-sum-fourth-powers, list-product-negative, list-count-positive-odd, list-count-negative-odd."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase159(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_seventeenth(self):
        self.check("(list-seventeenth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18))", 17)

    def test_sum_fourth_powers(self):
        self.check("(list-sum-fourth-powers '(1 2 3))", 98)
        self.check("(list-sum-fourth-powers '())", 0)

    def test_product_negative(self):
        self.check("(list-product-negative '(-2 3 -4 5))", 8)
        self.check("(list-product-negative '())", 1)

    def test_count_positive_odd(self):
        self.check("(list-count-positive-odd '(-3 1 2 3 5 6))", 3)
        self.check("(list-count-positive-odd '())", 0)

    def test_count_negative_odd(self):
        self.check("(list-count-negative-odd '(-3 -2 -1 0 1))", 2)
        self.check("(list-count-negative-odd '())", 0)


if __name__ == "__main__":
    unittest.main()
