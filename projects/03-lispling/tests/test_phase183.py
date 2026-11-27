"""Phase 183: list-forty-first, list-sum-twenty-eighth-powers, list-count/sum-multiples-of-twenty-six, list-product-multiples-of-twenty-five."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase183(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_nth(self):
        self.check("(list-forty-first '(" + " ".join(str(i) for i in range(1, 43)) + "))", 41)
        self.check("(list-forty-first '(1 2))", [])

    def test_sum_powers(self):
        self.check("(list-sum-twenty-eighth-powers '(1 2 3))", 1 + 2**28 + 3**28)
        self.check("(list-sum-twenty-eighth-powers '())", 0)
        self.check("(list-sum-twenty-eighth-powers '(-2))", 2**28)

    def test_count_multiples(self):
        self.check("(list-count-multiples-of-twenty-six '(26 27 52 78 79))", 3)
        self.check("(list-count-multiples-of-twenty-six '())", 0)

    def test_sum_multiples(self):
        self.check("(list-sum-multiples-of-twenty-six '(26 27 52 78 79))", 156)
        self.check("(list-sum-multiples-of-twenty-six '(1 2))", 0)

    def test_product_multiples(self):
        self.check("(list-product-multiples-of-twenty-five '(25 26 50))", 1250)
        self.check("(list-product-multiples-of-twenty-five '(1 2))", 1)


if __name__ == "__main__":
    unittest.main()
