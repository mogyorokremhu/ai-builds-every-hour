"""Phase 46: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase46(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_sums(self):
        self.check("(sum-odds '(1 2 3 4 5))", 9)
        self.check("(sum-abs '(-1 2 -3))", 6)
        self.check("(count-negatives '(-1 2 -3))", 2)

    def test_lists(self):
        self.check("(square-all '(1 2 3))", [1, 4, 9])
        self.check("(double-all '(1 2 3))", [2, 4, 6])
        self.check("(list-range-inclusive 2 5)", [2, 3, 4, 5])
        self.check("(list-range-inclusive 5 2)", [])
        self.check("(take-while-positive '(1 2 -1 3))", [1, 2])
