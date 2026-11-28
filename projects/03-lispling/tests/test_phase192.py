"""Phase 192: list-fiftieth, list-sum-thirty-seventh-powers, list-count/sum-multiples-of-thirty-five, list-product-multiples-of-thirty-four."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase192(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-fiftieth '(" + " ".join(str(i) for i in range(1, 52)) + "))", 50)
        self.check("(list-fiftieth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-thirty-seventh-powers '(1 2 3))", 1 + 2**37 + 3**37)
        self.check("(list-sum-thirty-seventh-powers '())", 0)
        self.check("(list-sum-thirty-seventh-powers '(-2))", -(2**37))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-thirty-five '(35 36 70 105 100))", 3)
        self.check("(list-count-multiples-of-thirty-five '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-thirty-five '(35 36 70 105 100))", 210)
        self.check("(list-sum-multiples-of-thirty-five '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-thirty-four '(34 35 68))", 2312)
        self.check("(list-product-multiples-of-thirty-four '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
