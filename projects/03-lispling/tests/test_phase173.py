"""Phase 173: list-thirty-first, list-sum-eighteenth-powers, list-count/sum-multiples-of-sixteen, list-product-multiples-of-fifteen."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase173(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_thirty_first(self):
        self.check("(list-thirty-first '(" + " ".join(str(i) for i in range(1, 33)) + "))", 31)
        self.check("(list-thirty-first '(1 2))", [])

    def test_sum_eighteenth_powers(self):
        self.check("(list-sum-eighteenth-powers '(1 2 3))", 1 + 2**18 + 3**18)
        self.check("(list-sum-eighteenth-powers '())", 0)
        self.check("(list-sum-eighteenth-powers '(-2))", 2**18)

    def test_count_multiples_of_sixteen(self):
        self.check("(list-count-multiples-of-sixteen '(16 17 32 48 49))", 3)
        self.check("(list-count-multiples-of-sixteen '())", 0)

    def test_sum_multiples_of_sixteen(self):
        self.check("(list-sum-multiples-of-sixteen '(16 17 32 48 49))", 96)
        self.check("(list-sum-multiples-of-sixteen '(-16 1))", -16)

    def test_product_multiples_of_fifteen(self):
        self.check("(list-product-multiples-of-fifteen '(15 16 30))", 450)
        self.check("(list-product-multiples-of-fifteen '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
