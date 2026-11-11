"""Phase 44: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase44(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_count_true(self):
        self.check("(count-true '(#t #f #t #t))", 3)

    def test_squares_average(self):
        self.check("(first-n-squares 4)", [1, 4, 9, 16])
        self.check("(average-by square '(1 3))", 5)

    def test_ends_wrap_mid_inc(self):
        self.check("(ends '(1 2 3 4))", [1, 4])
        self.check("(wrap-index 7 5)", 2)
        self.check("(wrap-index -1 5)", 4)
        self.check("(mid-range '(2 8 4))", 5)
        self.check("(inc-all '(1 2 3))", [2, 3, 4])
