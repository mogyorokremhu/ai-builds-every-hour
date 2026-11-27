"""Phase 175: list-thirty-third, list-sum-twentieth-powers, list-count/sum-multiples-of-eighteen, list-product-multiples-of-seventeen."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase175(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_thirty_third(self):
        self.check("(list-thirty-third '(" + " ".join(str(i) for i in range(1, 35)) + "))", 33)
        self.check("(list-thirty-third '(1 2))", [])

    def test_sum_twentieth_powers(self):
        self.check("(list-sum-twentieth-powers '(1 2 3))", 1 + 2**20 + 3**20)
        self.check("(list-sum-twentieth-powers '())", 0)
        self.check("(list-sum-twentieth-powers '(-2))", 2**20)

    def test_count_multiples_of_eighteen(self):
        self.check("(list-count-multiples-of-eighteen '(18 19 36 54 55))", 3)
        self.check("(list-count-multiples-of-eighteen '())", 0)

    def test_sum_multiples_of_eighteen(self):
        self.check("(list-sum-multiples-of-eighteen '(18 19 36 54 55))", 108)
        self.check("(list-sum-multiples-of-eighteen '(-18 1))", -18)

    def test_product_multiples_of_seventeen(self):
        self.check("(list-product-multiples-of-seventeen '(17 18 34))", 578)
        self.check("(list-product-multiples-of-seventeen '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
