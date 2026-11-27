"""Phase 184: list-forty-second, list-sum-twenty-ninth-powers, list-count/sum-multiples-of-twenty-seven, list-product-multiples-of-twenty-six."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase184(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-forty-second '(" + " ".join(str(i) for i in range(1, 44)) + "))", 42)
        self.check("(list-forty-second '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-twenty-ninth-powers '(1 2 3))", 1 + 2**29 + 3**29)
        self.check("(list-sum-twenty-ninth-powers '())", 0)
        self.check("(list-sum-twenty-ninth-powers '(-2))", -(2**29))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-twenty-seven '(27 28 54 81 82))", 3)
        self.check("(list-count-multiples-of-twenty-seven '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-twenty-seven '(27 28 54 81 82))", 162)
        self.check("(list-sum-multiples-of-twenty-seven '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-twenty-six '(26 27 52))", 1352)
        self.check("(list-product-multiples-of-twenty-six '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
