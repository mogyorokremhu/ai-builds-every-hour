"""Phase 187: list-forty-fifth, list-sum-thirty-second-powers, list-count/sum-multiples-of-thirty, list-product-multiples-of-twenty-nine."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase187(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-forty-fifth '(" + " ".join(str(i) for i in range(1, 47)) + "))", 45)
        self.check("(list-forty-fifth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-thirty-second-powers '(1 2 3))", 1 + 2**32 + 3**32)
        self.check("(list-sum-thirty-second-powers '())", 0)
        self.check("(list-sum-thirty-second-powers '(-2))", 2**32)

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-thirty '(30 31 60 90 91))", 3)
        self.check("(list-count-multiples-of-thirty '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-thirty '(30 31 60 90 91))", 180)
        self.check("(list-sum-multiples-of-thirty '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-twenty-nine '(29 30 58))", 1682)
        self.check("(list-product-multiples-of-twenty-nine '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
