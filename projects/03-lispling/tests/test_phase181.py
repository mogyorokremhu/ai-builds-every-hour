"""Phase 181: list-thirty-ninth, list-sum-twenty-sixth-powers, list-count/sum-multiples-of-twenty-four, list-product-multiples-of-twenty-three."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase181(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-thirty-ninth '(" + " ".join(str(i) for i in range(1, 39+2)) + "))", 39)
        self.check("(list-thirty-ninth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-twenty-sixth-powers '(1 2 3))", 1 + 2**26 + 3**26)
        self.check("(list-sum-twenty-sixth-powers '())", 0)
        self.check("(list-sum-twenty-sixth-powers '(-2))", (2**26))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-twenty-four '(24 25 48 72 73))", 3)
        self.check("(list-count-multiples-of-twenty-four '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-twenty-four '(24 25 48 72 73))", 144)
        self.check("(list-sum-multiples-of-twenty-four '(-24 1))", -24)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-twenty-three '(23 24 46))", 1058)
        self.check("(list-product-multiples-of-twenty-three '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
