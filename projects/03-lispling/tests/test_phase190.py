"""Phase 190: list-forty-eighth, list-sum-thirty-fifth-powers, list-count/sum-multiples-of-thirty-three, list-product-multiples-of-thirty-two."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase190(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-forty-eighth '(" + " ".join(str(i) for i in range(1, 50)) + "))", 48)
        self.check("(list-forty-eighth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-thirty-fifth-powers '(1 2 3))", 1 + 2**35 + 3**35)
        self.check("(list-sum-thirty-fifth-powers '())", 0)
        self.check("(list-sum-thirty-fifth-powers '(-2))", -(2**35))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-thirty-three '(33 34 66 99 100))", 3)
        self.check("(list-count-multiples-of-thirty-three '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-thirty-three '(33 34 66 99 100))", 198)
        self.check("(list-sum-multiples-of-thirty-three '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-thirty-two '(32 33 64))", 2048)
        self.check("(list-product-multiples-of-thirty-two '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
