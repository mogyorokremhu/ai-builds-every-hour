"""Phase 146: list-fourth, list-sum-odd, list-sum-even, list-count-lt, list-first-or."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase146(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_fourth(self):
        self.check("(list-fourth '(4 5 6 7 8))", 7)

    def test_sum_odd(self):
        self.check("(list-sum-odd '(1 2 3 4 5))", 9)
        self.check("(list-sum-odd '())", 0)

    def test_sum_even(self):
        self.check("(list-sum-even '(1 2 3 4 5))", 6)

    def test_count_lt(self):
        self.check("(list-count-lt 3 '(1 2 3 4))", 2)

    def test_first_or(self):
        self.check("(list-first-or 0 '())", 0)
        self.check("(list-first-or 0 '(7 8))", 7)


if __name__ == "__main__":
    unittest.main()
