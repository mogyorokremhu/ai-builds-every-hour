"""Phase 191: list-forty-ninth, list-sum-thirty-sixth-powers, list-count/sum-multiples-of-thirty-four, list-product-multiples-of-thirty-three."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase191(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-forty-ninth '(" + " ".join(str(i) for i in range(1, 51)) + "))", 49)
        self.check("(list-forty-ninth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-thirty-sixth-powers '(1 2 3))", 1 + 2**36 + 3**36)
        self.check("(list-sum-thirty-sixth-powers '())", 0)
        self.check("(list-sum-thirty-sixth-powers '(-2))", 2**36)

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-thirty-four '(34 35 68 102 100))", 3)
        self.check("(list-count-multiples-of-thirty-four '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-thirty-four '(34 35 68 102 100))", 204)
        self.check("(list-sum-multiples-of-thirty-four '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-thirty-three '(33 34 66))", 2178)
        self.check("(list-product-multiples-of-thirty-three '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
