"""Phase 147: list-fifth, list-count-eq, list-sum-positive, list-count-negative, list-last-or."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase147(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_fifth(self):
        self.check("(list-fifth '(1 2 3 4 5 6))", 5)

    def test_count_eq(self):
        self.check("(list-count-eq 2 '(1 2 2 3 2))", 3)
        self.check("(list-count-eq 9 '())", 0)

    def test_sum_positive(self):
        self.check("(list-sum-positive '(-1 2 -3 4))", 6)

    def test_count_negative(self):
        self.check("(list-count-negative '(-1 2 -3 4 0))", 2)

    def test_last_or(self):
        self.check("(list-last-or 0 '())", 0)
        self.check("(list-last-or 0 '(7 8 9))", 9)


if __name__ == "__main__":
    unittest.main()
