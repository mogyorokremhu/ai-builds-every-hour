"""Phase 161: list-nineteenth, list-sum-sixth-powers, list-count-multiples-of-four, list-sum-multiples-of-four, list-product-multiples-of-three."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase161(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nineteenth(self):
        self.check("(list-nineteenth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20))", 19)

    def test_sum_sixth_powers(self):
        self.check("(list-sum-sixth-powers '(1 2 3))", 794)
        self.check("(list-sum-sixth-powers '())", 0)

    def test_count_multiples_of_four(self):
        self.check("(list-count-multiples-of-four '(4 5 8 12 13))", 3)
        self.check("(list-count-multiples-of-four '())", 0)

    def test_sum_multiples_of_four(self):
        self.check("(list-sum-multiples-of-four '(4 5 8 12 13))", 24)
        self.check("(list-sum-multiples-of-four '(-4 1))", -4)

    def test_product_multiples_of_three(self):
        self.check("(list-product-multiples-of-three '(3 4 6 9))", 162)
        self.check("(list-product-multiples-of-three '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
