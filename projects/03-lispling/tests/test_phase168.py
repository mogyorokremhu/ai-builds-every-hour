"""Phase 168: list-twenty-sixth, list-sum-thirteenth-powers, list-count/sum-multiples-of-eleven, list-product-multiples-of-ten."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase168(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_twenty_sixth(self):
        self.check("(list-twenty-sixth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27))", 26)
        self.check("(list-twenty-sixth '(1 2))", [])

    def test_sum_thirteenth_powers(self):
        self.check("(list-sum-thirteenth-powers '(1 2 3))", 1 + 8192 + 1594323)
        self.check("(list-sum-thirteenth-powers '())", 0)
        self.check("(list-sum-thirteenth-powers '(-2))", -8192)

    def test_count_multiples_of_eleven(self):
        self.check("(list-count-multiples-of-eleven '(11 12 22 33 35))", 3)
        self.check("(list-count-multiples-of-eleven '())", 0)

    def test_sum_multiples_of_eleven(self):
        self.check("(list-sum-multiples-of-eleven '(11 12 22 33 35))", 66)
        self.check("(list-sum-multiples-of-eleven '(-11 1))", -11)

    def test_product_multiples_of_ten(self):
        self.check("(list-product-multiples-of-ten '(10 11 20 30))", 6000)
        self.check("(list-product-multiples-of-ten '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
