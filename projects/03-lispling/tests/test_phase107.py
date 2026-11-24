"""Phase 107: rolling sum*max, sum*min, mean*max, mean*min."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase107(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_sum_times_max(self):
        for v in self.each("(rolling-sum-times-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [162, 324, 288])

    def test_sum_times_min(self):
        for v in self.each("(rolling-sum-times-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 162, 72])

    def test_mean_times_max(self):
        for v in self.each("(rolling-mean-times-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 108, 96])

    def test_mean_times_min(self):
        for v in self.each("(rolling-mean-times-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 54, 24])


if __name__ == "__main__":
    unittest.main()
