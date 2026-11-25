"""Phase 118: rolling mean/sum/median/range to the fourth power."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase118(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (3 6 9) (6 9 12) (9 12 3)
    def test_mean_fourth(self):
        # means 6, 9, 8
        for v in self.each("(rolling-mean-fourth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [1296, 6561, 4096])

    def test_sum_fourth(self):
        # sums 18, 27, 24
        for v in self.each("(rolling-sum-fourth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [104976, 531441, 331776])

    def test_median_fourth(self):
        # medians 6, 9, 9
        for v in self.each("(rolling-median-fourth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [1296, 6561, 6561])

    def test_range_fourth(self):
        # ranges 6, 6, 9
        for v in self.each("(rolling-range-fourth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [1296, 1296, 6561])


if __name__ == "__main__":
    unittest.main()
