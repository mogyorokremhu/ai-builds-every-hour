"""Phase 164: list-twenty-second, list-sum-ninth-powers, list-count/sum-multiples-of-seven, list-product-multiples-of-six."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase164(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_twenty_second(self):
        self.check("(list-twenty-second '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23))", 22)
        self.check("(list-twenty-second '(1 2))", [])

    def test_sum_ninth_powers(self):
        self.check("(list-sum-ninth-powers '(1 2 3))", 1 + 512 + 19683)
        self.check("(list-sum-ninth-powers '())", 0)
        self.check("(list-sum-ninth-powers '(-1))", -1)

    def test_count_multiples_of_seven(self):
        self.check("(list-count-multiples-of-seven '(7 8 14 21 22))", 3)
        self.check("(list-count-multiples-of-seven '())", 0)

    def test_sum_multiples_of_seven(self):
        self.check("(list-sum-multiples-of-seven '(7 8 14 21 22))", 42)
        self.check("(list-sum-multiples-of-seven '(-7 1))", -7)

    def test_product_multiples_of_six(self):
        self.check("(list-product-multiples-of-six '(6 7 12 18))", 6 * 12 * 18)
        self.check("(list-product-multiples-of-six '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
