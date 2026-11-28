"""Phase 200: list-fifty-eighth, list-sum-forty-fifth-powers, list-count/sum-multiples-of-forty-three, list-product-multiples-of-forty-two."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase200(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-fifty-eighth '(" + " ".join(str(i) for i in range(1, 60)) + "))", 58)
        self.check("(list-fifty-eighth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-forty-fifth-powers '(1 2 3))", 1 + 2**45 + 3**45)
        self.check("(list-sum-forty-fifth-powers '())", 0)
        self.check("(list-sum-forty-fifth-powers '(-2))", -(2**45))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-forty-three '(43 44 86 129 100))", 3)
        self.check("(list-count-multiples-of-forty-three '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-forty-three '(43 44 86 129 100))", 258)
        self.check("(list-sum-multiples-of-forty-three '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-forty-two '(42 43 84))", 3528)
        self.check("(list-product-multiples-of-forty-two '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
