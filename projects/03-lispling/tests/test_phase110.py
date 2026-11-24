"""Phase 110: rolling median*max, median*min, range*max, range*min."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase110(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_median_times_max(self):
        # windows (3 6 9) (6 9 12) (9 12 3): medians 6, 9, 9; maxes 9, 12, 12
        for v in self.each("(rolling-median-times-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 108, 108])

    def test_median_times_min(self):
        for v in self.each("(rolling-median-times-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 54, 27])

    def test_range_times_max(self):
        # ranges 6, 6, 9
        for v in self.each("(rolling-range-times-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 72, 108])

    def test_range_times_min(self):
        for v in self.each("(rolling-range-times-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 36, 27])


if __name__ == "__main__":
    unittest.main()
