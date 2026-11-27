"""Phase 189: list-forty-seventh, list-sum-thirty-fourth-powers, list-count/sum-multiples-of-thirty-two, list-product-multiples-of-thirty-one."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase189(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-forty-seventh '(" + " ".join(str(i) for i in range(1, 49)) + "))", 47)
        self.check("(list-forty-seventh '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-thirty-fourth-powers '(1 2 3))", 1 + 2**34 + 3**34)
        self.check("(list-sum-thirty-fourth-powers '())", 0)
        self.check("(list-sum-thirty-fourth-powers '(-2))", 2**34)

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-thirty-two '(32 33 64 96 97))", 3)
        self.check("(list-count-multiples-of-thirty-two '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-thirty-two '(32 33 64 96 97))", 192)
        self.check("(list-sum-multiples-of-thirty-two '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-thirty-one '(31 32 62))", 1922)
        self.check("(list-product-multiples-of-thirty-one '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
