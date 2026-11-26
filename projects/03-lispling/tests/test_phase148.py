"""Phase 148: list-sixth, list-sum-negative, list-count-positive, list-count-zero, list-count-nonzero."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase148(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_sixth(self):
        self.check("(list-sixth '(1 2 3 4 5 6 7))", 6)

    def test_sum_negative(self):
        self.check("(list-sum-negative '(-1 2 -3 4))", -4)
        self.check("(list-sum-negative '())", 0)

    def test_count_positive(self):
        self.check("(list-count-positive '(-1 2 0 4))", 2)

    def test_count_zero(self):
        self.check("(list-count-zero '(0 1 0 2 0))", 3)

    def test_count_nonzero(self):
        self.check("(list-count-nonzero '(0 1 0 2 0))", 2)


if __name__ == "__main__":
    unittest.main()
