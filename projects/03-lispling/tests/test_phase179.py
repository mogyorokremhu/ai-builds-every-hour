"""Phase 179: list-thirty-seventh, list-sum-twenty-fourth-powers, list-count/sum-multiples-of-twenty-two, list-product-multiples-of-twenty-one."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase179(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-thirty-seventh '(" + " ".join(str(i) for i in range(1, 37+2)) + "))", 37)
        self.check("(list-thirty-seventh '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-twenty-fourth-powers '(1 2 3))", 1 + 2**24 + 3**24)
        self.check("(list-sum-twenty-fourth-powers '())", 0)
        self.check("(list-sum-twenty-fourth-powers '(-2))", 2**24)

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-twenty-two '(22 23 44 66 67))", 3)
        self.check("(list-count-multiples-of-twenty-two '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-twenty-two '(22 23 44 66 67))", 132)
        self.check("(list-sum-multiples-of-twenty-two '(-22 1))", -22)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-twenty-one '(21 22 42))", 882)
        self.check("(list-product-multiples-of-twenty-one '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
