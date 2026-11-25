"""Phase 125: rolling mean/sum/median/range to the eighth power."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase125(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_mean_eighth(self):
        for v in self.each("(rolling-mean-eighth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [2**8, 3**8, 4**8])

    def test_sum_eighth(self):
        for v in self.each("(rolling-sum-eighth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [6**8, 9**8, 12**8])

    def test_median_eighth(self):
        for v in self.each("(rolling-median-eighth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [2**8, 3**8, 4**8])

    def test_range_eighth(self):
        for v in self.each("(rolling-range-eighth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [2**8, 2**8, 2**8])


if __name__ == "__main__":
    unittest.main()
