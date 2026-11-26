"""Phase 157: list-fifteenth, list-count-positive-even, list-sum-squares-odd, list-weighted-sum, list-count-prime."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase157(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_fifteenth(self):
        self.check("(list-fifteenth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16))", 15)

    def test_count_positive_even(self):
        self.check("(list-count-positive-even '(-2 0 2 4 5 6))", 3)
        self.check("(list-count-positive-even '())", 0)

    def test_sum_squares_odd(self):
        self.check("(list-sum-squares-odd '(1 2 3 4 5))", 35)
        self.check("(list-sum-squares-odd '())", 0)

    def test_weighted_sum(self):
        self.check("(list-weighted-sum '(5 6 7))", 20)
        self.check("(list-weighted-sum '())", 0)

    def test_count_prime(self):
        self.check("(list-count-prime '(1 2 3 4 5 6 7 8 9 10))", 4)
        self.check("(list-count-prime '())", 0)


if __name__ == "__main__":
    unittest.main()
