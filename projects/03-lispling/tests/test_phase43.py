"""Phase 43: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase43(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_product_none(self):
        self.check("(product-by square '(1 2 3))", 36)
        self.check("(none? even? '(1 3 5))", True)
        self.check("(none? even? '(1 2 5))", False)

    def test_second_last_nth_or(self):
        self.check("(second-last '(1 2 3 4))", 3)
        self.check("(nth-or '(10 20) 1 0)", 20)
        self.check("(nth-or '(10 20) 5 -1)", -1)

    def test_sign_between_diff(self):
        self.check("(sign -7)", -1)
        self.check("(sign 0)", 0)
        self.check("(sign 9)", 1)
        self.check("(between? 5 1 10)", True)
        self.check("(between? 11 1 10)", False)
        self.check("(abs-diff 3 10)", 7)
        self.check("(abs-diff 10 3)", 7)
