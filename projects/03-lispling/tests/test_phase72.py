"""Phase 72: rolling-percent-change, rolling-mad, rolling-zscore-last, rolling-distinct."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase72(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_percent_change(self):
        for v in self.each("(rolling-percent-change '(100 110 121) 2)"):
            self.assertEqual(len(v), 2)
            self.assertAlmostEqual(v[0], 10)
            self.assertAlmostEqual(v[1], 10)

    def test_mad(self):
        for v in self.each("(rolling-mad '(1 2 3 4) 3)"):
            self.assertAlmostEqual(v[0], 2 / 3)
            self.assertAlmostEqual(v[1], 2 / 3)

    def test_zscore_last(self):
        for v in self.each("(rolling-zscore-last '(1 2 3 4) 3)"):
            self.assertEqual(len(v), 2)
            self.assertGreater(v[0], 0)

    def test_zscore_constant(self):
        for v in self.each("(rolling-zscore-last '(5 5 5) 3)"):
            self.assertEqual(v, [0.0])

    def test_distinct(self):
        for v in self.each("(rolling-distinct '(1 1 2 2 3) 3)"):
            self.assertEqual(v, [2, 2, 2])


if __name__ == "__main__":
    unittest.main()
