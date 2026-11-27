"""Phase 167: list-twenty-fifth, list-sum-twelfth-powers, list-count/sum-multiples-of-ten, list-product-multiples-of-nine."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase167(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_twenty_fifth(self):
        self.check("(list-twenty-fifth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26))", 25)
        self.check("(list-twenty-fifth '(1 2))", [])

    def test_sum_twelfth_powers(self):
        self.check("(list-sum-twelfth-powers '(1 2 3))", 1 + 4096 + 531441)
        self.check("(list-sum-twelfth-powers '())", 0)
        self.check("(list-sum-twelfth-powers '(-2))", 4096)

    def test_count_multiples_of_ten(self):
        self.check("(list-count-multiples-of-ten '(10 11 20 30 35))", 3)
        self.check("(list-count-multiples-of-ten '())", 0)

    def test_sum_multiples_of_ten(self):
        self.check("(list-sum-multiples-of-ten '(10 11 20 30 35))", 60)
        self.check("(list-sum-multiples-of-ten '(-10 1))", -10)

    def test_product_multiples_of_nine(self):
        self.check("(list-product-multiples-of-nine '(9 10 18 27))", 9 * 18 * 27)
        self.check("(list-product-multiples-of-nine '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
