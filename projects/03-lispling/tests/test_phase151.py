"""Phase 151: list-ninth, list-count-odd, list-count-neq, list-sum-ge, list-sum-le."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase151(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_ninth(self):
        self.check("(list-ninth '(1 2 3 4 5 6 7 8 9 10))", 9)

    def test_count_odd(self):
        self.check("(list-count-odd '(1 2 3 4 5))", 3)
        self.check("(list-count-odd '())", 0)

    def test_count_neq(self):
        self.check("(list-count-neq 2 '(1 2 3 2))", 2)

    def test_sum_ge(self):
        self.check("(list-sum-ge 3 '(1 2 3 4 5))", 12)

    def test_sum_le(self):
        self.check("(list-sum-le 3 '(1 2 3 4 5))", 6)


if __name__ == "__main__":
    unittest.main()
