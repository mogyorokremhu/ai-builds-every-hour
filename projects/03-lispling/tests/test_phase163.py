"""Phase 163: list-twenty-first, list-sum-eighth-powers, list-count/sum-multiples-of-six, list-product-multiples-of-five."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase163(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_twenty_first(self):
        self.check("(list-twenty-first '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22))", 21)
        self.check("(list-twenty-first '(1 2))", [])

    def test_sum_eighth_powers(self):
        self.check("(list-sum-eighth-powers '(1 2 3))", 1 + 256 + 6561)
        self.check("(list-sum-eighth-powers '())", 0)

    def test_count_multiples_of_six(self):
        self.check("(list-count-multiples-of-six '(6 7 12 18 19))", 3)
        self.check("(list-count-multiples-of-six '())", 0)

    def test_sum_multiples_of_six(self):
        self.check("(list-sum-multiples-of-six '(6 7 12 18 19))", 36)
        self.check("(list-sum-multiples-of-six '(-6 1))", -6)

    def test_product_multiples_of_five(self):
        self.check("(list-product-multiples-of-five '(5 6 10 15))", 750)
        self.check("(list-product-multiples-of-five '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
