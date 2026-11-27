"""Phase 182: list-fortieth, list-sum-twenty-seventh-powers, list-count/sum-multiples-of-twenty-five, list-product-multiples-of-twenty-four."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase182(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-fortieth '(" + " ".join(str(i) for i in range(1, 40+2)) + "))", 40)
        self.check("(list-fortieth '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-twenty-seventh-powers '(1 2 3))", 1 + 2**27 + 3**27)
        self.check("(list-sum-twenty-seventh-powers '())", 0)
        self.check("(list-sum-twenty-seventh-powers '(-2))", -(2**27))

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-twenty-five '(25 26 50 75 76))", 3)
        self.check("(list-count-multiples-of-twenty-five '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-twenty-five '(25 26 50 75 76))", 150)
        self.check("(list-sum-multiples-of-twenty-five '(-25 1))", -25)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-twenty-four '(24 25 48))", 1152)
        self.check("(list-product-multiples-of-twenty-four '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
