"""Phase 145: list-third, list-sum-abs, list-last-index, list-repeat-each, list-count-gt."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase145(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_third(self):
        self.check("(list-third '(4 5 6 7))", 6)

    def test_sum_abs(self):
        self.check("(list-sum-abs '(-1 2 -3))", 6)
        self.check("(list-sum-abs '())", 0)

    def test_last_index(self):
        self.check("(list-last-index 2 '(2 1 2 3))", 2)
        self.check("(list-last-index 9 '(1 2))", -1)

    def test_repeat_each(self):
        self.check("(list-repeat-each 2 '(1 2 3))", [1, 1, 2, 2, 3, 3])
        self.check("(list-repeat-each 0 '(1 2))", [])

    def test_count_gt(self):
        self.check("(list-count-gt 2 '(1 2 3 4))", 2)


if __name__ == "__main__":
    unittest.main()
