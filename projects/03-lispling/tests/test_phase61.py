"""Phase 61: sum-absolute-deviations, pearson-skewness, median-absolute-deviation, weighted-variance."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase61(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_sum_abs_dev(self):
        for v in self.each("(sum-absolute-deviations '(2 4 4 4 5 5 7 9))"):
            self.assertAlmostEqual(float(v), 12.0)

    def test_skew(self):
        # mean 5, median 4.5, std 2 -> 3*0.5/2
        for v in self.each("(pearson-skewness '(2 4 4 4 5 5 7 9))"):
            self.assertAlmostEqual(float(v), 0.75)

    def test_mad_median(self):
        for v in self.each("(median-absolute-deviation '(1 1 2 2 4 6 9))"):
            self.assertAlmostEqual(float(v), 1.0)

    def test_weighted_variance(self):
        # mean = (1+2+6)/4 = 2.25 ; var = (1.5625+.0625+2*.5625)/4 = 0.6875
        for v in self.each("(weighted-variance '(1 2 3) '(1 1 2))"):
            self.assertAlmostEqual(float(v), 0.6875)


if __name__ == "__main__":
    unittest.main()
