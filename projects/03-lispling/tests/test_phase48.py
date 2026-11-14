"""Phase 48: list/number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase48(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_numbers(self):
        self.check("(sum-of-cubes '(1 2 3))", 36)
        self.check("(count-zeros '(0 1 0 2))", 2)
        self.check("(sum-positives '(-1 2 3))", 5)

    def test_lists(self):
        self.check("(negatives '(-1 2 -3 4))", [-1, -3])
        self.check("(take-while-negative '(-1 -2 3 -4))", [-1, -2])
        self.check("(quadruple-all '(1 2 3))", [4, 8, 12])
        self.check("(list-range-step-down 5 2)", [5, 4, 3, 2])
        self.check("(list-range-step-down 2 5)", [])
