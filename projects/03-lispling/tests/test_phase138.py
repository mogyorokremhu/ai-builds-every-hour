"""Phase 138: list-sum, list-count-of, list-sum-of, list-all-equal?."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase138(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_sum(self):
        self.check("(list-sum '(1 2 3 4))", 10)
        self.check("(list-sum '())", 0)

    def test_count_of(self):
        self.check("(list-count-of 2 '(1 2 2 3))", 2)

    def test_sum_of(self):
        self.check("(list-sum-of abs '(1 -2 3))", 6)

    def test_all_equal(self):
        self.check("(list-all-equal? '(1 1 1))", True)
        self.check("(list-all-equal? '(1 2))", False)
        self.check("(list-all-equal? '())", True)


if __name__ == "__main__":
    unittest.main()
