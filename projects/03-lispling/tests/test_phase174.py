"""Phase 174: list-thirty-second, list-sum-nineteenth-powers, list-count/sum-multiples-of-seventeen, list-product-multiples-of-sixteen."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase174(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_thirty_second(self):
        self.check("(list-thirty-second '(" + " ".join(str(i) for i in range(1, 34)) + "))", 32)
        self.check("(list-thirty-second '(1 2))", [])

    def test_sum_nineteenth_powers(self):
        self.check("(list-sum-nineteenth-powers '(1 2 3))", 1 + 2**19 + 3**19)
        self.check("(list-sum-nineteenth-powers '())", 0)
        self.check("(list-sum-nineteenth-powers '(-2))", -(2**19))

    def test_count_multiples_of_seventeen(self):
        self.check("(list-count-multiples-of-seventeen '(17 18 34 51 52))", 3)
        self.check("(list-count-multiples-of-seventeen '())", 0)

    def test_sum_multiples_of_seventeen(self):
        self.check("(list-sum-multiples-of-seventeen '(17 18 34 51 52))", 102)
        self.check("(list-sum-multiples-of-seventeen '(-17 1))", -17)

    def test_product_multiples_of_sixteen(self):
        self.check("(list-product-multiples-of-sixteen '(16 17 32))", 512)
        self.check("(list-product-multiples-of-sixteen '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
