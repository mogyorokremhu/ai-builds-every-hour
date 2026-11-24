"""Phase 111: rolling sum*mean, first*mean, last*mean, median*mean."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase111(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (3 6 9) (6 9 12) (9 12 3): sums 18, 27, 24; means 6, 9, 8
    def test_sum_times_mean(self):
        for v in self.each("(rolling-sum-times-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [108, 243, 192])

    def test_first_times_mean(self):
        for v in self.each("(rolling-first-times-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 54, 72])

    def test_last_times_mean(self):
        for v in self.each("(rolling-last-times-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 108, 24])

    def test_median_times_mean(self):
        for v in self.each("(rolling-median-times-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [36, 81, 72])


if __name__ == "__main__":
    unittest.main()
