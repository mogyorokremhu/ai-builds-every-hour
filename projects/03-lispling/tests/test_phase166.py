"""Phase 166: list-twenty-fourth, list-sum-eleventh-powers, list-count/sum-multiples-of-nine, list-product-multiples-of-eight."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase166(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_twenty_fourth(self):
        self.check("(list-twenty-fourth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25))", 24)
        self.check("(list-twenty-fourth '(1 2))", [])

    def test_sum_eleventh_powers(self):
        self.check("(list-sum-eleventh-powers '(1 2 3))", 1 + 2048 + 177147)
        self.check("(list-sum-eleventh-powers '())", 0)
        self.check("(list-sum-eleventh-powers '(-2))", -2048)

    def test_count_multiples_of_nine(self):
        self.check("(list-count-multiples-of-nine '(9 10 18 27 28))", 3)
        self.check("(list-count-multiples-of-nine '())", 0)

    def test_sum_multiples_of_nine(self):
        self.check("(list-sum-multiples-of-nine '(9 10 18 27 28))", 54)
        self.check("(list-sum-multiples-of-nine '(-9 1))", -9)

    def test_product_multiples_of_eight(self):
        self.check("(list-product-multiples-of-eight '(8 9 16 24))", 8 * 16 * 24)
        self.check("(list-product-multiples-of-eight '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
