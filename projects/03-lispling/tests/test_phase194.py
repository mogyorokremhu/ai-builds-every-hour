"""Phase 194: list-fifty-second, list-sum-thirty-ninth-powers, list-count/sum-multiples-of-thirty-seven, list-product-multiples-of-thirty-six."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase194(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-fifty-second '(" + " ".join(str(i) for i in range(1, 54)) + "))", 52)
        self.check("(list-fifty-second '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-thirty-ninth-powers '(1 2 3))", 1 + 2**39 + 3**39)
        self.check("(list-sum-thirty-ninth-powers '())", 0)
        self.check("(list-sum-thirty-ninth-powers '(-2))", -(2**39))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-thirty-seven '(37 38 74 111 100))", 3)
        self.check("(list-count-multiples-of-thirty-seven '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-thirty-seven '(37 38 74 111 100))", 222)
        self.check("(list-sum-multiples-of-thirty-seven '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-thirty-six '(36 37 72))", 2592)
        self.check("(list-product-multiples-of-thirty-six '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
