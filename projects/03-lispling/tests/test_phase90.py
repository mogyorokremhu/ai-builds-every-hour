"""Phase 90: rolling mean/min/median gaps."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))
# windows of '(3 6 9 12 3) size 3: means 6, 9, 8; medians 6, 9, 9


class TestPhase90(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_mean_minus_first(self):
        for v in self.each("(rolling-mean-minus-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [3, 3, -1])

    def test_mean_minus_last(self):
        for v in self.each("(rolling-mean-minus-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [-3, -3, 5])

    def test_min_minus_median(self):
        for v in self.each("(rolling-min-minus-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [-3, -3, -6])

    def test_median_minus_max(self):
        for v in self.each("(rolling-median-minus-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [-3, -3, -3])


if __name__ == "__main__":
    unittest.main()
