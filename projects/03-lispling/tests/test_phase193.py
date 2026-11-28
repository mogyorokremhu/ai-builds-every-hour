"""Phase 193: list-fifty-first, list-sum-thirty-eighth-powers, list-count/sum-multiples-of-thirty-six, list-product-multiples-of-thirty-five."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase193(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-fifty-first '(" + " ".join(str(i) for i in range(1, 53)) + "))", 51)
        self.check("(list-fifty-first '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-thirty-eighth-powers '(1 2 3))", 1 + 2**38 + 3**38)
        self.check("(list-sum-thirty-eighth-powers '())", 0)
        self.check("(list-sum-thirty-eighth-powers '(-2))", 2**38)

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-thirty-six '(36 37 72 108 100))", 3)
        self.check("(list-count-multiples-of-thirty-six '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-thirty-six '(36 37 72 108 100))", 216)
        self.check("(list-sum-multiples-of-thirty-six '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-thirty-five '(35 36 70))", 2450)
        self.check("(list-product-multiples-of-thirty-five '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
