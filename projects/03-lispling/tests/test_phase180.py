"""Phase 180: list-thirty-eighth, list-sum-twenty-fifth-powers, list-count/sum-multiples-of-twenty-three, list-product-multiples-of-twenty-two."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase180(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-thirty-eighth '(" + " ".join(str(i) for i in range(1, 38+2)) + "))", 38)
        self.check("(list-thirty-eighth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-twenty-fifth-powers '(1 2 3))", 1 + 2**25 + 3**25)
        self.check("(list-sum-twenty-fifth-powers '())", 0)
        self.check("(list-sum-twenty-fifth-powers '(-2))", -(2**25))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-twenty-three '(23 24 46 69 70))", 3)
        self.check("(list-count-multiples-of-twenty-three '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-twenty-three '(23 24 46 69 70))", 138)
        self.check("(list-sum-multiples-of-twenty-three '(-23 1))", -23)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-twenty-two '(22 23 44))", 968)
        self.check("(list-product-multiples-of-twenty-two '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
