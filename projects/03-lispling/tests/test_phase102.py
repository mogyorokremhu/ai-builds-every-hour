"""Phase 102: rolling first*last, max*min, range-mean, range-median."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase102(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_first_times_last(self):
        for v in self.each("(rolling-first-times-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [27, 72, 27])

    def test_max_times_min(self):
        for v in self.each("(rolling-max-times-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [27, 72, 36])

    def test_range_minus_mean(self):
        for v in self.each("(rolling-range-minus-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [0, -3, 1])

    def test_range_minus_median(self):
        for v in self.each("(rolling-range-minus-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [0, -3, 0])


if __name__ == "__main__":
    unittest.main()
