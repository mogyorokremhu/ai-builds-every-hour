"""Phase 162: list-twentieth, list-sum-seventh-powers, list-count-multiples-of-five, list-sum-multiples-of-five, list-product-multiples-of-four."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase162(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_twentieth(self):
        self.check("(list-twentieth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21))", 20)
        self.check("(list-twentieth '(1 2))", [])

    def test_sum_seventh_powers(self):
        self.check("(list-sum-seventh-powers '(1 2 3))", 2316)
        self.check("(list-sum-seventh-powers '())", 0)

    def test_count_multiples_of_five(self):
        self.check("(list-count-multiples-of-five '(5 6 10 15 16))", 3)
        self.check("(list-count-multiples-of-five '())", 0)

    def test_sum_multiples_of_five(self):
        self.check("(list-sum-multiples-of-five '(5 6 10 15 16))", 30)
        self.check("(list-sum-multiples-of-five '(-5 1))", -5)

    def test_product_multiples_of_four(self):
        self.check("(list-product-multiples-of-four '(4 5 8 12))", 384)
        self.check("(list-product-multiples-of-four '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
