"""Phase 152: list-tenth, list-product-lt, list-product-ge, list-count-divisible, list-sum-divisible."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase152(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_tenth(self):
        self.check("(list-tenth '(1 2 3 4 5 6 7 8 9 10 11))", 10)

    def test_product_lt(self):
        self.check("(list-product-lt 4 '(1 2 3 4 5))", 6)
        self.check("(list-product-lt 0 '(1 2))", 1)

    def test_product_ge(self):
        self.check("(list-product-ge 4 '(1 2 3 4 5))", 20)

    def test_count_divisible(self):
        self.check("(list-count-divisible 3 '(3 4 6 9 10))", 3)

    def test_sum_divisible(self):
        self.check("(list-sum-divisible 3 '(3 4 6 9 10))", 18)


if __name__ == "__main__":
    unittest.main()
