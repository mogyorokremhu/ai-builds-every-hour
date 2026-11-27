"""Phase 176: list-thirty-fourth, list-sum-twenty-first-powers, list-count/sum-multiples-of-nineteen, list-product-multiples-of-eighteen."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase176(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_thirty_fourth(self):
        self.check("(list-thirty-fourth '(" + " ".join(str(i) for i in range(1, 36)) + "))", 34)
        self.check("(list-thirty-fourth '(1 2))", [])

    def test_sum_twenty_first_powers(self):
        self.check("(list-sum-twenty-first-powers '(1 2 3))", 1 + 2**21 + 3**21)
        self.check("(list-sum-twenty-first-powers '())", 0)
        self.check("(list-sum-twenty-first-powers '(-2))", -(2**21))

    def test_count_multiples_of_nineteen(self):
        self.check("(list-count-multiples-of-nineteen '(19 20 38 57 58))", 3)
        self.check("(list-count-multiples-of-nineteen '())", 0)

    def test_sum_multiples_of_nineteen(self):
        self.check("(list-sum-multiples-of-nineteen '(19 20 38 57 58))", 114)
        self.check("(list-sum-multiples-of-nineteen '(-19 1))", -19)

    def test_product_multiples_of_eighteen(self):
        self.check("(list-product-multiples-of-eighteen '(18 19 36))", 648)
        self.check("(list-product-multiples-of-eighteen '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
