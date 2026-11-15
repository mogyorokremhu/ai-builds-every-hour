"""Phase 66: mean-bias, smape, normalized-rmse, cumulative-error."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase66(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_mean_bias(self):
        for v in self.each("(mean-bias '(1 2 3) '(2 4 3))"):
            self.assertAlmostEqual(float(v), 1.0)

    def test_smape(self):
        for v in self.each("(smape '(100 200) '(110 180))"):
            self.assertAlmostEqual(float(v), 100 * (20 / 210 + 40 / 380) / 2)

    def test_smape_perfect(self):
        for v in self.each("(smape '(1 2 3) '(1 2 3))"):
            self.assertAlmostEqual(float(v), 0.0)

    def test_normalized_rmse(self):
        for v in self.each("(normalized-rmse '(0 10) '(3 10))"):
            self.assertAlmostEqual(float(v), (4.5 ** 0.5) / 10)

    def test_cumulative_error(self):
        for v in self.each("(cumulative-error '(1 2 3) '(2 4 3))"):
            self.assertEqual([float(x) for x in list(v)], [1.0, 3.0, 3.0])


if __name__ == "__main__":
    unittest.main()
