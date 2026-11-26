"""Phase 144: list-second, list-sum-squares, list-index-where, list-min-max, list-clamp-all."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase144(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_second(self):
        self.check("(list-second '(4 5 6))", 5)

    def test_sum_squares(self):
        self.check("(list-sum-squares '(1 2 3))", 14)
        self.check("(list-sum-squares '())", 0)

    def test_index_where(self):
        self.check("(list-index-where (lambda (x) (> x 2)) '(1 2 3 4))", 2)
        self.check("(list-index-where (lambda (x) (> x 9)) '(1 2 3))", -1)

    def test_min_max(self):
        self.check("(list-min-max '(3 1 4 1 5))", [1, 5])
        self.check("(list-min-max '(7))", [7, 7])

    def test_clamp_all(self):
        self.check("(list-clamp-all 0 10 '(-5 3 15))", [0, 3, 10])


if __name__ == "__main__":
    unittest.main()
