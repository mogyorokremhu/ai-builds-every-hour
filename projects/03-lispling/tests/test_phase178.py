"""Phase 178: list-thirty-sixth, list-sum-twenty-third-powers, list-count/sum-multiples-of-twenty-one, list-product-multiples-of-twenty."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase178(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_thirty_sixth(self):
        self.check("(list-thirty-sixth '(" + " ".join(str(i) for i in range(1, 38)) + "))", 36)
        self.check("(list-thirty-sixth '(1 2))", [])

    def test_sum_twenty_third_powers(self):
        self.check("(list-sum-twenty-third-powers '(1 2 3))", 1 + 2**23 + 3**23)
        self.check("(list-sum-twenty-third-powers '())", 0)
        self.check("(list-sum-twenty-third-powers '(-2))", -(2**23))

    def test_count_multiples_of_twenty_one(self):
        self.check("(list-count-multiples-of-twenty-one '(21 22 42 63 64))", 3)
        self.check("(list-count-multiples-of-twenty-one '())", 0)

    def test_sum_multiples_of_twenty_one(self):
        self.check("(list-sum-multiples-of-twenty-one '(21 22 42 63 64))", 126)
        self.check("(list-sum-multiples-of-twenty-one '(-21 1))", -21)

    def test_product_multiples_of_twenty(self):
        self.check("(list-product-multiples-of-twenty '(20 21 40))", 800)
        self.check("(list-product-multiples-of-twenty '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
