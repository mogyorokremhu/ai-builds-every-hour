"""Phase 98: rolling mean+median, mean+first, mean+last, sum+median."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase98(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_mean_plus_median(self):
        for v in self.each("(rolling-mean-plus-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [12, 18, 17])

    def test_mean_plus_first(self):
        for v in self.each("(rolling-mean-plus-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 15, 17])

    def test_mean_plus_last(self):
        for v in self.each("(rolling-mean-plus-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [15, 21, 11])

    def test_sum_plus_median(self):
        for v in self.each("(rolling-sum-plus-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [24, 36, 33])


if __name__ == "__main__":
    unittest.main()
