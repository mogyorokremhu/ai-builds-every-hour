"""Phase 201: list-fifty-ninth, list-sum-forty-sixth-powers, list-count/sum-multiples-of-forty-four, list-product-multiples-of-forty-three."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase201(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-fifty-ninth '(" + " ".join(str(i) for i in range(1, 61)) + "))", 59)
        self.check("(list-fifty-ninth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-forty-sixth-powers '(1 2 3))", 1 + 2**46 + 3**46)
        self.check("(list-sum-forty-sixth-powers '())", 0)
        self.check("(list-sum-forty-sixth-powers '(-2))", 2**46)

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-forty-four '(44 45 88 132 100))", 3)
        self.check("(list-count-multiples-of-forty-four '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-forty-four '(44 45 88 132 100))", 264)
        self.check("(list-sum-multiples-of-forty-four '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-forty-three '(43 44 86))", 3698)
        self.check("(list-product-multiples-of-forty-three '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
