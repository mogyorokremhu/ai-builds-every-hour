"""Phase 185: list-forty-third, list-sum-thirtieth-powers, list-count/sum-multiples-of-twenty-eight, list-product-multiples-of-twenty-seven."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase185(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-forty-third '(" + " ".join(str(i) for i in range(1, 45)) + "))", 43)
        self.check("(list-forty-third '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-thirtieth-powers '(1 2 3))", 1 + 2**30 + 3**30)
        self.check("(list-sum-thirtieth-powers '())", 0)
        self.check("(list-sum-thirtieth-powers '(-2))", 2**30)

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-twenty-eight '(28 29 56 84 85))", 3)
        self.check("(list-count-multiples-of-twenty-eight '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-twenty-eight '(28 29 56 84 85))", 168)
        self.check("(list-sum-multiples-of-twenty-eight '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-twenty-seven '(27 28 54))", 1458)
        self.check("(list-product-multiples-of-twenty-seven '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
