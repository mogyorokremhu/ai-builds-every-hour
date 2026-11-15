"""Phase 62: skewness, excess-kurtosis, kurtosis, cumulative-mean."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))
DATA = "'(2 4 4 4 5 5 7 9)"


class TestPhase62(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_skewness(self):
        # m3 = 42/8 = 5.25, sd = 2 -> 5.25 / 8
        for v in self.each(f"(skewness {DATA})"):
            self.assertAlmostEqual(float(v), 0.65625)

    def test_excess_kurtosis(self):
        # m4 = 356/8 = 44.5, var = 4 -> 44.5/16 - 3
        for v in self.each(f"(excess-kurtosis {DATA})"):
            self.assertAlmostEqual(float(v), -0.21875)

    def test_kurtosis(self):
        for v in self.each(f"(kurtosis {DATA})"):
            self.assertAlmostEqual(float(v), 2.78125)

    def test_cumulative_mean(self):
        for v in self.each("(cumulative-mean '(2 4 6 8))"):
            self.assertEqual([float(x) for x in v], [2.0, 3.0, 4.0, 5.0])


if __name__ == "__main__":
    unittest.main()
