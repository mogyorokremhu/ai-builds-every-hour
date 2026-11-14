"""Phase 54: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase54(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_numbers(self):
        self.check("(sum-less-than 3 '(1 2 3 4))", 3)
        self.check("(sum-greater-than 2 '(1 2 3 4))", 7)
        self.check("(count-multiples-between 2 3 9 '(2 4 6 8 10))", 3)

    def test_lists(self):
        self.check("(decuple-all '(1 2))", [10, 20])
        self.check("(evens-doubled '(1 2 3 4))", [4, 8])
        self.check("(odds-doubled '(1 2 3))", [2, 6])
        self.check("(take-while-less-than 3 '(1 2 3 1))", [1, 2])
