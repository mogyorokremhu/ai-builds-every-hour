"""Phase 70: rolling-std-dev, rolling-sum-squares, rolling-geometric-mean, rolling-midrange."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase70(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_rolling_std_dev(self):
        for v in self.each("(rolling-std-dev '(1 2 3 4 5) 3)"):
            self.assertEqual(len(v), 3)
            self.assertAlmostEqual(v[0], v[2])
            self.assertGreater(v[0], 0)

    def test_rolling_sum_squares(self):
        for v in self.each("(rolling-sum-squares '(1 2 3 4) 2)"):
            self.assertEqual(v, [5.0, 13.0, 25.0])

    def test_rolling_geometric_mean(self):
        for v in self.each("(rolling-geometric-mean '(1 4 16 64) 2)"):
            for a, b in zip(v, [2.0, 8.0, 32.0]):
                self.assertAlmostEqual(a, b)

    def test_rolling_midrange(self):
        for v in self.each("(rolling-midrange '(1 9 3 7) 2)"):
            self.assertEqual(v, [5.0, 6.0, 5.0])

    def test_short_input(self):
        for v in self.each("(rolling-std-dev '(1 2) 3)"):
            self.assertEqual(v, [])


if __name__ == "__main__":
    unittest.main()
