"""Phase 165: list-twenty-third, list-sum-tenth-powers, list-count/sum-multiples-of-eight, list-product-multiples-of-seven."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase165(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_twenty_third(self):
        self.check("(list-twenty-third '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24))", 23)
        self.check("(list-twenty-third '(1 2))", [])

    def test_sum_tenth_powers(self):
        self.check("(list-sum-tenth-powers '(1 2 3))", 1 + 1024 + 59049)
        self.check("(list-sum-tenth-powers '())", 0)
        self.check("(list-sum-tenth-powers '(-2))", 1024)

    def test_count_multiples_of_eight(self):
        self.check("(list-count-multiples-of-eight '(8 9 16 24 25))", 3)
        self.check("(list-count-multiples-of-eight '())", 0)

    def test_sum_multiples_of_eight(self):
        self.check("(list-sum-multiples-of-eight '(8 9 16 24 25))", 48)
        self.check("(list-sum-multiples-of-eight '(-8 1))", -8)

    def test_product_multiples_of_seven(self):
        self.check("(list-product-multiples-of-seven '(7 8 14 21))", 7 * 14 * 21)
        self.check("(list-product-multiples-of-seven '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
