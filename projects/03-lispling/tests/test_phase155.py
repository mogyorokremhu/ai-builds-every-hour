"""Phase 155: list-thirteenth, list-sum-above-mean, list-sum-below-mean, list-sum-even-index, list-sum-odd-index."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase155(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_thirteenth(self):
        self.check("(list-thirteenth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14))", 13)

    def test_sum_above_mean(self):
        self.check("(list-sum-above-mean '(1 2 3 4 10))", 10)
        self.check("(list-sum-above-mean '())", 0)

    def test_sum_below_mean(self):
        self.check("(list-sum-below-mean '(1 2 3 4 10))", 6)
        self.check("(list-sum-below-mean '())", 0)

    def test_sum_even_index(self):
        self.check("(list-sum-even-index '(1 2 3 4 5))", 9)

    def test_sum_odd_index(self):
        self.check("(list-sum-odd-index '(1 2 3 4 5))", 6)
        self.check("(list-sum-odd-index '())", 0)


if __name__ == "__main__":
    unittest.main()
