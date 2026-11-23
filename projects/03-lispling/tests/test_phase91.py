"""Phase 91: rolling sum/median/first/last gaps."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))
# windows of '(3 6 9 12 3) size 3: sums 18, 27, 24; medians 6, 9, 9


class TestPhase91(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_sum_minus_first(self):
        for v in self.each("(rolling-sum-minus-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [15, 21, 15])

    def test_sum_minus_last(self):
        for v in self.each("(rolling-sum-minus-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 15, 21])

    def test_median_minus_last(self):
        for v in self.each("(rolling-median-minus-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [-3, -3, 6])

    def test_first_minus_median(self):
        for v in self.each("(rolling-first-minus-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [-3, -3, 0])


if __name__ == "__main__":
    unittest.main()
