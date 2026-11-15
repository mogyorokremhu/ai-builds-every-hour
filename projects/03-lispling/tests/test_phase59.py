"""Phase 59: root-mean-square, harmonic-mean, geometric-mean, trimmed-mean."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase59(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_rms(self):
        for v in self.each("(root-mean-square '(3 4))"):
            self.assertAlmostEqual(float(v), (12.5) ** 0.5)

    def test_harmonic(self):
        for v in self.each("(harmonic-mean '(1 2 4))"):
            self.assertAlmostEqual(float(v), 12 / 7)

    def test_geometric(self):
        for v in self.each("(geometric-mean '(2 8))"):
            self.assertAlmostEqual(float(v), 4.0)

    def test_trimmed(self):
        for v in self.each("(trimmed-mean '(100 1 2 3 -50) 1)"):
            self.assertAlmostEqual(float(v), 2.0)


if __name__ == "__main__":
    unittest.main()
