"""Phase 63: mean-absolute-error, mean-squared-error, root-mean-squared-error, running-min."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase63(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_mae(self):
        for v in self.each("(mean-absolute-error '(1 2 3 4) '(2 2 5 4))"):
            self.assertAlmostEqual(float(v), 0.75)

    def test_mse(self):
        for v in self.each("(mean-squared-error '(1 2 3 4) '(2 2 5 4))"):
            self.assertAlmostEqual(float(v), 1.25)

    def test_rmse(self):
        for v in self.each("(root-mean-squared-error '(0 0) '(3 4))"):
            self.assertAlmostEqual(float(v), 12.5 ** 0.5)

    def test_running_min(self):
        for v in self.each("(running-min '(5 3 4 1 2))"):
            self.assertEqual(list(v), [5, 3, 3, 1, 1])

    def test_running_min_empty(self):
        for v in self.each("(running-min '())"):
            self.assertEqual(list(v) if v else [], [])


if __name__ == "__main__":
    unittest.main()
