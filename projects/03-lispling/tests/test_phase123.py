"""Phase 123: rolling mean/sum/median/range to the seventh power."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase123(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (1 2 3) (2 3 4) (3 4 5): means 2 3 4, sums 6 9 12, medians 2 3 4, ranges 2 2 2
    def test_mean_seventh(self):
        for v in self.each("(rolling-mean-seventh '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [128, 2187, 16384])

    def test_sum_seventh(self):
        for v in self.each("(rolling-sum-seventh '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [6**7, 9**7, 12**7])

    def test_median_seventh(self):
        for v in self.each("(rolling-median-seventh '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [128, 2187, 16384])

    def test_range_seventh(self):
        for v in self.each("(rolling-range-seventh '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [128, 128, 128])


if __name__ == "__main__":
    unittest.main()
