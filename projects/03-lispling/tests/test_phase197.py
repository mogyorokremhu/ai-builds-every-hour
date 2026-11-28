"""Phase 197: list-fifty-fifth, list-sum-forty-second-powers, list-count/sum-multiples-of-forty, list-product-multiples-of-thirty-nine."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase197(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-fifty-fifth '(" + " ".join(str(i) for i in range(1, 57)) + "))", 55)
        self.check("(list-fifty-fifth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-forty-second-powers '(1 2 3))", 1 + 2**42 + 3**42)
        self.check("(list-sum-forty-second-powers '())", 0)
        self.check("(list-sum-forty-second-powers '(-2))", 2**42)

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-forty '(40 41 80 120 100))", 3)
        self.check("(list-count-multiples-of-forty '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-forty '(40 41 80 120 100))", 240)
        self.check("(list-sum-multiples-of-forty '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-thirty-nine '(39 40 78))", 3042)
        self.check("(list-product-multiples-of-thirty-nine '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
