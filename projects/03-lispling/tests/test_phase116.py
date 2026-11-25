"""Phase 116: rolling sum/median/range cubed and mean squared."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase116(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (3 6 9) (6 9 12) (9 12 3): sums 18 27 24, medians 6 9 9, ranges 6 6 9, means 6 9 8
    def test_sum_cubed(self):
        for v in self.each("(rolling-sum-cubed '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [5832, 19683, 13824])

    def test_median_cubed(self):
        for v in self.each("(rolling-median-cubed '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [216, 729, 729])

    def test_range_cubed(self):
        for v in self.each("(rolling-range-cubed '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [216, 216, 729])

    def test_mean_squared(self):
        for v in self.each("(rolling-mean-squared '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [36, 81, 64])


if __name__ == "__main__":
    unittest.main()
