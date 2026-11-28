"""Phase 196: list-fifty-fourth, list-sum-forty-first-powers, list-count/sum-multiples-of-thirty-nine, list-product-multiples-of-thirty-eight."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase196(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-fifty-fourth '(" + " ".join(str(i) for i in range(1, 56)) + "))", 54)
        self.check("(list-fifty-fourth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-forty-first-powers '(1 2 3))", 1 + 2**41 + 3**41)
        self.check("(list-sum-forty-first-powers '())", 0)
        self.check("(list-sum-forty-first-powers '(-2))", -(2**41))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-thirty-nine '(39 40 78 117 100))", 3)
        self.check("(list-count-multiples-of-thirty-nine '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-thirty-nine '(39 40 78 117 100))", 234)
        self.check("(list-sum-multiples-of-thirty-nine '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-thirty-eight '(38 39 76))", 2888)
        self.check("(list-product-multiples-of-thirty-eight '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
