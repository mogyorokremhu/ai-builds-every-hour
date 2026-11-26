"""Phase 156: list-fourteenth, list-sum-mod, list-count-mod, list-product-mod, list-count-at-mean."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase156(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_fourteenth(self):
        self.check("(list-fourteenth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15))", 14)

    def test_sum_mod(self):
        self.check("(list-sum-mod '(1 2 3 4 5 6 7) 3 1)", 12)
        self.check("(list-sum-mod '() 3 1)", 0)

    def test_count_mod(self):
        self.check("(list-count-mod '(1 2 3 4 5 6 7) 3 1)", 3)

    def test_product_mod(self):
        self.check("(list-product-mod '(1 2 3 4 5 6 7) 3 1)", 28)
        self.check("(list-product-mod '() 3 1)", 1)

    def test_count_at_mean(self):
        self.check("(list-count-at-mean '(1 2 3 4 5))", 1)
        self.check("(list-count-at-mean '(2 2 2))", 3)
        self.check("(list-count-at-mean '())", 0)


if __name__ == "__main__":
    unittest.main()
