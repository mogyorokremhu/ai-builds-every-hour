"""Phase 149: list-seventh, list-count-ge, list-count-le, list-sum-gt, list-sum-lt."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase149(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_seventh(self):
        self.check("(list-seventh '(1 2 3 4 5 6 7 8))", 7)

    def test_count_ge(self):
        self.check("(list-count-ge 3 '(1 3 5 2 4))", 3)
        self.check("(list-count-ge 3 '())", 0)

    def test_count_le(self):
        self.check("(list-count-le 3 '(1 3 5 2 4))", 3)

    def test_sum_gt(self):
        self.check("(list-sum-gt 2 '(1 3 5 2 4))", 12)

    def test_sum_lt(self):
        self.check("(list-sum-lt 3 '(1 3 5 2 4))", 3)


if __name__ == "__main__":
    unittest.main()
