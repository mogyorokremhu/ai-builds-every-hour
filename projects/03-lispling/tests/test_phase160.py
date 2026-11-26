"""Phase 160: list-eighteenth, list-sum-fifth-powers, list-product-nonzero, list-count-multiples-of-three, list-sum-multiples-of-three."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase160(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_eighteenth(self):
        self.check("(list-eighteenth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19))", 18)

    def test_sum_fifth_powers(self):
        self.check("(list-sum-fifth-powers '(1 2 3))", 276)
        self.check("(list-sum-fifth-powers '())", 0)

    def test_product_nonzero(self):
        self.check("(list-product-nonzero '(2 0 3 0 4))", 24)
        self.check("(list-product-nonzero '())", 1)

    def test_count_multiples_of_three(self):
        self.check("(list-count-multiples-of-three '(3 4 6 9 10))", 3)
        self.check("(list-count-multiples-of-three '())", 0)

    def test_sum_multiples_of_three(self):
        self.check("(list-sum-multiples-of-three '(3 4 6 9 10))", 18)
        self.check("(list-sum-multiples-of-three '(-3 1))", -3)


if __name__ == "__main__":
    unittest.main()
