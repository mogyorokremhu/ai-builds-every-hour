"""Phase 203: list-sixty-first, list-sum-forty-eighth-powers, list-count/sum-multiples-of-forty-six, list-product-multiples-of-forty-five."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase203(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-sixty-first '(" + " ".join(str(i) for i in range(1, 63)) + "))", 61)
        self.check("(list-sixty-first '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-forty-eighth-powers '(1 2 3))", 1 + 2**48 + 3**48)
        self.check("(list-sum-forty-eighth-powers '())", 0)
        self.check("(list-sum-forty-eighth-powers '(-2))", 2**48)

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-forty-six '(46 47 92 138 100))", 3)
        self.check("(list-count-multiples-of-forty-six '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-forty-six '(46 47 92 138 100))", 276)
        self.check("(list-sum-multiples-of-forty-six '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-forty-five '(45 46 90))", 4050)
        self.check("(list-product-multiples-of-forty-five '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
