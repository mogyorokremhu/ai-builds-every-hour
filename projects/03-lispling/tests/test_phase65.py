"""Phase 65: predict-linear, residuals, max-error, mean-absolute-percentage-error."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase65(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_predict(self):
        for v in self.each("(predict-linear '(1 2 3 4) '(3 5 7 9) 10)"):
            self.assertAlmostEqual(float(v), 21.0)

    def test_residuals_perfect(self):
        for v in self.each("(residuals '(1 2 3 4) '(3 5 7 9))"):
            for r in list(v):
                self.assertAlmostEqual(float(r), 0.0)

    def test_residuals_sum_zero(self):
        for v in self.each("(residuals '(1 2 3) '(1 3 2))"):
            self.assertAlmostEqual(sum(float(r) for r in list(v)), 0.0)

    def test_max_error(self):
        for v in self.each("(max-error '(1 2 3) '(1 5 2))"):
            self.assertEqual(v, 3)

    def test_mape(self):
        for v in self.each("(mean-absolute-percentage-error '(100 200) '(110 180))"):
            self.assertAlmostEqual(float(v), 10.0)


if __name__ == "__main__":
    unittest.main()
