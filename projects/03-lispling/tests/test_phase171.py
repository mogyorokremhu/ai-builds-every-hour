"""Phase 171: list-twenty-ninth, list-sum-sixteenth-powers, list-count/sum-multiples-of-fourteen, list-product-multiples-of-thirteen."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase171(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_twenty_ninth(self):
        self.check("(list-twenty-ninth '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30))", 29)
        self.check("(list-twenty-ninth '(1 2))", [])

    def test_sum_sixteenth_powers(self):
        self.check("(list-sum-sixteenth-powers '(1 2 3))", 1 + 65536 + 43046721)
        self.check("(list-sum-sixteenth-powers '())", 0)
        self.check("(list-sum-sixteenth-powers '(-2))", 65536)

    def test_count_multiples_of_fourteen(self):
        self.check("(list-count-multiples-of-fourteen '(14 15 28 42 43))", 3)
        self.check("(list-count-multiples-of-fourteen '())", 0)

    def test_sum_multiples_of_fourteen(self):
        self.check("(list-sum-multiples-of-fourteen '(14 15 28 42 43))", 84)
        self.check("(list-sum-multiples-of-fourteen '(-14 1))", -14)

    def test_product_multiples_of_thirteen(self):
        self.check("(list-product-multiples-of-thirteen '(13 14 26))", 338)
        self.check("(list-product-multiples-of-thirteen '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
