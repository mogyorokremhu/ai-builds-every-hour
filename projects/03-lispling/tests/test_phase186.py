"""Phase 186: list-forty-fourth, list-sum-thirty-first-powers, list-count/sum-multiples-of-twenty-nine, list-product-multiples-of-twenty-eight."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase186(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-forty-fourth '(" + " ".join(str(i) for i in range(1, 46)) + "))", 44)
        self.check("(list-forty-fourth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-thirty-first-powers '(1 2 3))", 1 + 2**31 + 3**31)
        self.check("(list-sum-thirty-first-powers '())", 0)
        self.check("(list-sum-thirty-first-powers '(-2))", -(2**31))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-twenty-nine '(29 30 58 87 88))", 3)
        self.check("(list-count-multiples-of-twenty-nine '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-twenty-nine '(29 30 58 87 88))", 174)
        self.check("(list-sum-multiples-of-twenty-nine '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-twenty-eight '(28 29 56))", 1568)
        self.check("(list-product-multiples-of-twenty-eight '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
