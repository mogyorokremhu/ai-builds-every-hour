"""Phase 169: list-twenty-seventh, list-sum-fourteenth-powers, list-count/sum-multiples-of-twelve, list-product-multiples-of-eleven."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase169(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_twenty_seventh(self):
        self.check("(list-twenty-seventh '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28))", 27)
        self.check("(list-twenty-seventh '(1 2))", [])

    def test_sum_fourteenth_powers(self):
        self.check("(list-sum-fourteenth-powers '(1 2 3))", 1 + 16384 + 4782969)
        self.check("(list-sum-fourteenth-powers '())", 0)
        self.check("(list-sum-fourteenth-powers '(-2))", 16384)

    def test_count_multiples_of_twelve(self):
        self.check("(list-count-multiples-of-twelve '(12 13 24 36 40))", 3)
        self.check("(list-count-multiples-of-twelve '())", 0)

    def test_sum_multiples_of_twelve(self):
        self.check("(list-sum-multiples-of-twelve '(12 13 24 36 40))", 72)
        self.check("(list-sum-multiples-of-twelve '(-12 1))", -12)

    def test_product_multiples_of_eleven(self):
        self.check("(list-product-multiples-of-eleven '(11 12 22))", 242)
        self.check("(list-product-multiples-of-eleven '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
