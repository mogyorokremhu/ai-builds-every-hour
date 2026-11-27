"""Phase 172: list-thirtieth, list-sum-seventeenth-powers, list-count/sum-multiples-of-fifteen, list-product-multiples-of-fourteen."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase172(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_thirtieth(self):
        self.check("(list-thirtieth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31))", 30)
        self.check("(list-thirtieth '(1 2))", [])

    def test_sum_seventeenth_powers(self):
        self.check("(list-sum-seventeenth-powers '(1 2 3))", 1 + 131072 + 129140163)
        self.check("(list-sum-seventeenth-powers '())", 0)
        self.check("(list-sum-seventeenth-powers '(-2))", -131072)

    def test_count_multiples_of_fifteen(self):
        self.check("(list-count-multiples-of-fifteen '(15 16 30 45 46))", 3)
        self.check("(list-count-multiples-of-fifteen '())", 0)

    def test_sum_multiples_of_fifteen(self):
        self.check("(list-sum-multiples-of-fifteen '(15 16 30 45 46))", 90)
        self.check("(list-sum-multiples-of-fifteen '(-15 1))", -15)

    def test_product_multiples_of_fourteen(self):
        self.check("(list-product-multiples-of-fourteen '(14 15 28))", 392)
        self.check("(list-product-multiples-of-fourteen '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
