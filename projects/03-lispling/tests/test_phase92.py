"""Phase 92: rolling sum vs max/min/mean/median gaps."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))
# windows of '(3 6 9 12 3) size 3: sums 18, 27, 24


class TestPhase92(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_sum_minus_max(self):
        for v in self.each("(rolling-sum-minus-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 15, 12])

    def test_sum_minus_min(self):
        for v in self.each("(rolling-sum-minus-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [15, 21, 21])

    def test_sum_minus_mean(self):
        for v in self.each("(rolling-sum-minus-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [12, 18, 16])

    def test_sum_minus_median(self):
        for v in self.each("(rolling-sum-minus-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [12, 18, 15])


if __name__ == "__main__":
    unittest.main()
