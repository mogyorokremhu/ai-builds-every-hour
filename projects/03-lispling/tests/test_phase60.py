"""Phase 60: sum-squared-deviations, coefficient-of-variation, standard-error, midrange-of."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase60(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_ssd(self):
        for v in self.each("(sum-squared-deviations '(1 2 3 4 5))"):
            self.assertAlmostEqual(float(v), 10.0)

    def test_cv(self):
        for v in self.each("(coefficient-of-variation '(2 4 4 4 5 5 7 9))"):
            self.assertAlmostEqual(float(v), 0.4)

    def test_se(self):
        for v in self.each("(standard-error '(2 4 4 4 5 5 7 9))"):
            self.assertAlmostEqual(float(v), 2 / 8 ** 0.5)

    def test_midrange(self):
        for v in self.each("(midrange-of '(1 9 4))"):
            self.assertAlmostEqual(float(v), 5.0)


if __name__ == "__main__":
    unittest.main()
