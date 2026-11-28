"""Phase 199: list-fifty-seventh, list-sum-forty-fourth-powers, list-count/sum-multiples-of-forty-two, list-product-multiples-of-forty-one."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase199(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-fifty-seventh '(" + " ".join(str(i) for i in range(1, 59)) + "))", 57)
        self.check("(list-fifty-seventh '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-forty-fourth-powers '(1 2 3))", 1 + 2**44 + 3**44)
        self.check("(list-sum-forty-fourth-powers '())", 0)
        self.check("(list-sum-forty-fourth-powers '(-2))", 2**44)

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-forty-two '(42 43 84 126 100))", 3)
        self.check("(list-count-multiples-of-forty-two '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-forty-two '(42 43 84 126 100))", 252)
        self.check("(list-sum-multiples-of-forty-two '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-forty-one '(41 42 82))", 3362)
        self.check("(list-product-multiples-of-forty-one '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
