"""Phase 64: linear-slope, linear-intercept, r-squared, running-max-min-range."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase64(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_slope(self):
        for v in self.each("(linear-slope '(1 2 3 4) '(3 5 7 9))"):
            self.assertAlmostEqual(float(v), 2.0)

    def test_intercept(self):
        for v in self.each("(linear-intercept '(1 2 3 4) '(3 5 7 9))"):
            self.assertAlmostEqual(float(v), 1.0)

    def test_r_squared_perfect(self):
        for v in self.each("(r-squared '(1 2 3 4) '(3 5 7 9))"):
            self.assertAlmostEqual(float(v), 1.0)

    def test_r_squared_partial(self):
        for v in self.each("(r-squared '(1 2 3) '(1 3 2))"):
            self.assertAlmostEqual(float(v), 0.25)

    def test_running_range(self):
        for v in self.each("(running-max-min-range '(5 3 8 1 9))"):
            self.assertEqual(list(v), [0, 2, 5, 7, 8])


if __name__ == "__main__":
    unittest.main()
