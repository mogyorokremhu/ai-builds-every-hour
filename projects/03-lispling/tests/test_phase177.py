"""Phase 177: list-thirty-fifth, list-sum-twenty-second-powers, list-count/sum-multiples-of-twenty, list-product-multiples-of-nineteen."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase177(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_thirty_fifth(self):
        self.check("(list-thirty-fifth '(" + " ".join(str(i) for i in range(1, 37)) + "))", 35)
        self.check("(list-thirty-fifth '(1 2))", [])

    def test_sum_twenty_second_powers(self):
        self.check("(list-sum-twenty-second-powers '(1 2 3))", 1 + 2**22 + 3**22)
        self.check("(list-sum-twenty-second-powers '())", 0)
        self.check("(list-sum-twenty-second-powers '(-2))", 2**22)

    def test_count_multiples_of_twenty(self):
        self.check("(list-count-multiples-of-twenty '(20 21 40 60 61))", 3)
        self.check("(list-count-multiples-of-twenty '())", 0)

    def test_sum_multiples_of_twenty(self):
        self.check("(list-sum-multiples-of-twenty '(20 21 40 60 61))", 120)
        self.check("(list-sum-multiples-of-twenty '(-20 1))", -20)

    def test_product_multiples_of_nineteen(self):
        self.check("(list-product-multiples-of-nineteen '(19 20 38))", 722)
        self.check("(list-product-multiples-of-nineteen '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
