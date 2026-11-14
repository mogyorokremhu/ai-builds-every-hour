"""Phase 47: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase47(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_numbers(self):
        self.check("(sum-squares '(1 2 3))", 14)
        self.check("(count-positives '(-1 2 3))", 2)
        self.check("(product-evens '(1 2 3 4))", 8)

    def test_lists(self):
        self.check("(drop-while-positive '(1 2 -1 3))", [-1, 3])
        self.check("(list-range-exclusive 2 5)", [2, 3, 4])
        self.check("(list-range-exclusive 5 2)", [])
        self.check("(triple-all '(1 2 3))", [3, 6, 9])
        self.check("(positives '(-1 2 -3 4))", [2, 4])
