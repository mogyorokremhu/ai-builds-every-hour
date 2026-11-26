"""Phase 158: list-sixteenth, list-count-perfect-square, list-sum-cubes, list-product-positive, list-count-negative-even."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase158(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_sixteenth(self):
        self.check("(list-sixteenth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17))", 16)

    def test_count_perfect_square(self):
        self.check("(list-count-perfect-square '(0 1 2 3 4 5 9 10 16))", 5)
        self.check("(list-count-perfect-square '())", 0)

    def test_sum_cubes(self):
        self.check("(list-sum-cubes '(1 2 3))", 36)
        self.check("(list-sum-cubes '())", 0)

    def test_product_positive(self):
        self.check("(list-product-positive '(-1 2 0 3 4))", 24)
        self.check("(list-product-positive '())", 1)

    def test_count_negative_even(self):
        self.check("(list-count-negative-even '(-4 -3 -2 0 2))", 2)
        self.check("(list-count-negative-even '())", 0)


if __name__ == "__main__":
    unittest.main()
