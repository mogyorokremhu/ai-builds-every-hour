"""Phase 188: list-forty-sixth, list-sum-thirty-third-powers, list-count/sum-multiples-of-thirty-one, list-product-multiples-of-thirty."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase188(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-forty-sixth '(" + " ".join(str(i) for i in range(1, 48)) + "))", 46)
        self.check("(list-forty-sixth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-thirty-third-powers '(1 2 3))", 1 + 2**33 + 3**33)
        self.check("(list-sum-thirty-third-powers '())", 0)
        self.check("(list-sum-thirty-third-powers '(-2))", -(2**33))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-thirty-one '(31 32 62 93 94))", 3)
        self.check("(list-count-multiples-of-thirty-one '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-thirty-one '(31 32 62 93 94))", 186)
        self.check("(list-sum-multiples-of-thirty-one '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-thirty '(30 31 60))", 1800)
        self.check("(list-product-multiples-of-thirty '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
