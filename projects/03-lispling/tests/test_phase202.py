"""Phase 202: list-sixtieth, list-sum-forty-seventh-powers, list-count/sum-multiples-of-forty-five, list-product-multiples-of-forty-four."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase202(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-sixtieth '(" + " ".join(str(i) for i in range(1, 62)) + "))", 60)
        self.check("(list-sixtieth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-forty-seventh-powers '(1 2 3))", 1 + 2**47 + 3**47)
        self.check("(list-sum-forty-seventh-powers '())", 0)
        self.check("(list-sum-forty-seventh-powers '(-2))", -(2**47))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-forty-five '(45 46 90 135 100))", 3)
        self.check("(list-count-multiples-of-forty-five '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-forty-five '(45 46 90 135 100))", 270)
        self.check("(list-sum-multiples-of-forty-five '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-forty-four '(44 45 88))", 3872)
        self.check("(list-product-multiples-of-forty-four '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
