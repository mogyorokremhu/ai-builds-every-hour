"""Phase 41: list helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase41(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_list_min_by(self):
        self.check("(list-min-by abs '(4 -1 3))", -1)

    def test_range_sum(self):
        self.check("(range-sum 1 10)", 55)
        self.check("(range-sum 5 1)", 0)

    def test_list_product(self):
        self.check("(list-product '(1 2 3 4))", 24)
        self.check("(list-product '())", 1)

    def test_second_third(self):
        self.check("(second '(1 2 3))", 2)
        self.check("(third '(1 2 3))", 3)

    def test_swap_pairs(self):
        self.check("(swap-pairs '(1 2 3 4 5))", [2, 1, 4, 3, 5])


if __name__ == "__main__":
    unittest.main()
