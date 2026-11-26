"""Phase 142: list-pad-left, list-pad-right, list-dedupe-adjacent, list-index-of-all, list-sum-by."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase142(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_pad_left(self):
        self.check("(list-pad-left 5 0 '(1 2))", [0, 0, 0, 1, 2])
        self.check("(list-pad-left 1 0 '(1 2))", [1, 2])

    def test_pad_right(self):
        self.check("(list-pad-right 4 9 '(1 2))", [1, 2, 9, 9])

    def test_dedupe_adjacent(self):
        self.check("(list-dedupe-adjacent '(1 1 2 2 2 1 3 3))", [1, 2, 1, 3])
        self.check("(list-dedupe-adjacent '())", [])

    def test_index_of_all(self):
        self.check("(list-index-of-all 2 '(2 1 2 3 2))", [0, 2, 4])
        self.check("(list-index-of-all 7 '(1 2))", [])

    def test_sum_by(self):
        self.check("(list-sum-by (lambda (x) (* x x)) '(1 2 3))", 14)


if __name__ == "__main__":
    unittest.main()
