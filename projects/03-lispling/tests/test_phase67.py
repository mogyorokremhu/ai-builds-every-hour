"""Phase 67: weighted-mean, exponential-moving-average, relative-error, median-absolute-error."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase67(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_weighted_mean(self):
        for v in self.each("(weighted-mean '(1 2 3) '(3 2 1))"):
            self.assertAlmostEqual(float(v), 10 / 6)

    def test_ema(self):
        for v in self.each("(exponential-moving-average '(10 20 30) 0.5)"):
            self.assertEqual([float(x) for x in list(v)], [10.0, 15.0, 22.5])

    def test_ema_empty(self):
        for v in self.each("(exponential-moving-average '() 0.5)"):
            self.assertEqual(list(v), [])

    def test_relative_error(self):
        for v in self.each("(relative-error 10 12)"):
            self.assertAlmostEqual(float(v), 0.2)

    def test_median_absolute_error(self):
        for v in self.each("(median-absolute-error '(1 2 3) '(2 4 3))"):
            self.assertAlmostEqual(float(v), 1.0)


if __name__ == "__main__":
    unittest.main()
