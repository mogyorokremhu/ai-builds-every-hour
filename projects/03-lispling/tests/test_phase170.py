"""Phase 170: list-twenty-eighth, list-sum-fifteenth-powers, list-count/sum-multiples-of-thirteen, list-product-multiples-of-twelve."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase170(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_twenty_eighth(self):
        self.check("(list-twenty-eighth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29))", 28)
        self.check("(list-twenty-eighth '(1 2))", [])

    def test_sum_fifteenth_powers(self):
        self.check("(list-sum-fifteenth-powers '(1 2 3))", 1 + 32768 + 14348907)
        self.check("(list-sum-fifteenth-powers '())", 0)
        self.check("(list-sum-fifteenth-powers '(-2))", -32768)

    def test_count_multiples_of_thirteen(self):
        self.check("(list-count-multiples-of-thirteen '(13 14 26 39 40))", 3)
        self.check("(list-count-multiples-of-thirteen '())", 0)

    def test_sum_multiples_of_thirteen(self):
        self.check("(list-sum-multiples-of-thirteen '(13 14 26 39 40))", 78)
        self.check("(list-sum-multiples-of-thirteen '(-13 1))", -13)

    def test_product_multiples_of_twelve(self):
        self.check("(list-product-multiples-of-twelve '(12 13 24))", 288)
        self.check("(list-product-multiples-of-twelve '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
