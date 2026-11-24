"""Phase 112: rolling range*mean, max*mean, min*mean, mean*mean."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase112(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (3 6 9) (6 9 12) (9 12 3): means 6, 9, 8
    def test_range_times_mean(self):
        for v in self.each("(rolling-range-times-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [36, 54, 72])

    def test_max_times_mean(self):
        for v in self.each("(rolling-max-times-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 108, 96])

    def test_min_times_mean(self):
        for v in self.each("(rolling-min-times-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 54, 24])

    def test_mean_times_mean(self):
        for v in self.each("(rolling-mean-times-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [36, 81, 64])


if __name__ == "__main__":
    unittest.main()
