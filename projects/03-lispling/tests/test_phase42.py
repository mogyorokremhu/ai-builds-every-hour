"""Phase 42: list helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase42(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_last_init(self):
        self.check("(last-element '(1 2 3))", 3)
        self.check("(init '(1 2 3))", [1, 2])

    def test_take_until_count_while(self):
        self.check("(take-until even? '(1 3 4 5))", [1, 3])
        self.check("(count-while odd? '(1 3 4 5))", 2)

    def test_sum_clamp(self):
        self.check("(sum-by square '(1 2 3))", 14)
        self.check("(clamp 15 0 10)", 10)
        self.check("(clamp -5 0 10)", 0)
        self.check("(clamp 5 0 10)", 5)
        self.check("(lerp 0 10 1)", 10)
