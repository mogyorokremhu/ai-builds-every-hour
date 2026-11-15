"""Phase 57: correlation, z-scores, min-max-normalize, moving-average."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase57(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_correlation(self):
        for v in self.each("(correlation '(1 2 3) '(2 4 6))"):
            self.assertAlmostEqual(v, 1.0)
        for v in self.each("(correlation '(1 2 3) '(6 4 2))"):
            self.assertAlmostEqual(v, -1.0)

    def test_z_scores(self):
        for v in self.each("(z-scores '(2 4 4 4 5 5 7 9))"):
            self.assertEqual(v, [-1.5, -0.5, -0.5, -0.5, 0, 0, 1, 2])

    def test_normalize(self):
        for v in self.each("(min-max-normalize '(10 20 30))"):
            self.assertEqual([float(x) for x in v], [0.0, 0.5, 1.0])

    def test_moving_average(self):
        for v in self.each("(moving-average '(1 2 3 4 5) 3)"):
            self.assertEqual([float(x) for x in v], [2.0, 3.0, 4.0])


if __name__ == "__main__":
    unittest.main()
