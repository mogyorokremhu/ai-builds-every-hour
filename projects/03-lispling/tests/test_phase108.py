"""Phase 108: rolling sum*median, mean*median, sum*range, mean*range."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase108(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_sum_times_median(self):
        for v in self.each("(rolling-sum-times-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [108, 243, 216])

    def test_mean_times_median(self):
        for v in self.each("(rolling-mean-times-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [36, 81, 72])

    def test_sum_times_range(self):
        for v in self.each("(rolling-sum-times-range '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [108, 162, 216])

    def test_mean_times_range(self):
        for v in self.each("(rolling-mean-times-range '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [36, 54, 72])


if __name__ == "__main__":
    unittest.main()
