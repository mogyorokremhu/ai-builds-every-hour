"""Phase 120: rolling mean/sum/median/range to the fifth power."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase120(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (3 6 9) (6 9 12) (9 12 3)
    def test_mean_fifth(self):
        for v in self.each("(rolling-mean-fifth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [7776, 59049, 32768])

    def test_sum_fifth(self):
        for v in self.each("(rolling-sum-fifth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [1889568, 14348907, 7962624])

    def test_median_fifth(self):
        for v in self.each("(rolling-median-fifth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [7776, 59049, 59049])

    def test_range_fifth(self):
        for v in self.each("(rolling-range-fifth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [7776, 7776, 59049])


if __name__ == "__main__":
    unittest.main()
