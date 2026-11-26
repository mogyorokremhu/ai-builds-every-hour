"""Phase 143: list-longest-run, list-count-runs, list-nth-or, list-product-by, list-swap."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase143(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_longest_run(self):
        self.check("(list-longest-run '(1 1 2 2 2 2 3))", 4)
        self.check("(list-longest-run '(5))", 1)
        self.check("(list-longest-run '())", 0)

    def test_count_runs(self):
        self.check("(list-count-runs '(1 1 2 2 2 1 3 3))", 4)
        self.check("(list-count-runs '())", 0)

    def test_nth_or(self):
        self.check("(list-nth-or 1 0 '(7 8 9))", 8)
        self.check("(list-nth-or 5 0 '(7 8 9))", 0)

    def test_product_by(self):
        self.check("(list-product-by (lambda (x) (+ x 1)) '(1 2 3))", 24)
        self.check("(list-product-by (lambda (x) x) '())", 1)

    def test_swap(self):
        self.check("(list-swap 0 2 '(1 2 3 4))", [3, 2, 1, 4])
        self.check("(list-swap 1 1 '(1 2 3))", [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
