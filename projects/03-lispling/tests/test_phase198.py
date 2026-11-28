"""Phase 198: list-fifty-sixth, list-sum-forty-third-powers, list-count/sum-multiples-of-forty-one, list-product-multiples-of-forty."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase198(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-fifty-sixth '(" + " ".join(str(i) for i in range(1, 58)) + "))", 56)
        self.check("(list-fifty-sixth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-forty-third-powers '(1 2 3))", 1 + 2**43 + 3**43)
        self.check("(list-sum-forty-third-powers '())", 0)
        self.check("(list-sum-forty-third-powers '(-2))", -(2**43))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-forty-one '(41 42 82 123 100))", 3)
        self.check("(list-count-multiples-of-forty-one '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-forty-one '(41 42 82 123 100))", 246)
        self.check("(list-sum-multiples-of-forty-one '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-forty '(40 41 80))", 3200)
        self.check("(list-product-multiples-of-forty '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
