"""Phase 69: rolling-mean, rolling-median, rolling-variance, rolling-product."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase69(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_rolling_mean(self):
        for v in self.each("(rolling-mean '(2 4 6 8 10) 3)"):
            self.assertEqual([float(x) for x in list(v)], [4.0, 6.0, 8.0])

    def test_rolling_median(self):
        for v in self.each("(rolling-median '(5 1 4 2 3) 3)"):
            self.assertEqual([float(x) for x in list(v)], [4.0, 2.0, 3.0])

    def test_rolling_variance(self):
        for v in self.each("(rolling-variance '(1 2 3 4 5) 3)"):
            vals = [float(x) for x in list(v)]
            self.assertEqual(len(vals), 3)
            self.assertAlmostEqual(vals[0], vals[2])
            self.assertGreater(vals[0], 0)

    def test_rolling_product(self):
        for v in self.each("(rolling-product '(1 2 3 4 5) 2)"):
            self.assertEqual([int(x) for x in list(v)], [2, 6, 12, 20])

    def test_short(self):
        for v in self.each("(rolling-mean '(1) 3)"):
            self.assertEqual(list(v), [])


if __name__ == "__main__":
    unittest.main()
