"""Phase 127: rolling mean, sum, median, range to the ninth power."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase127(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_mean_ninth(self):
        for v in self.each("(rolling-mean-ninth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [2**9,3**9,4**9])

    def test_sum_ninth(self):
        for v in self.each("(rolling-sum-ninth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [6**9,9**9,12**9])

    def test_median_ninth(self):
        for v in self.each("(rolling-median-ninth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [2**9,3**9,4**9])

    def test_range_ninth(self):
        for v in self.each("(rolling-range-ninth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [2**9,2**9,2**9])


if __name__ == "__main__":
    unittest.main()
