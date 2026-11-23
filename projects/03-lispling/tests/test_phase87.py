"""Phase 87: rolling max/min vs first, median vs mean gaps."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase87(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_max_minus_first(self):
        for v in self.each("(rolling-max-minus-first '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [4, 4, 6])

    def test_first_minus_min(self):
        for v in self.each("(rolling-first-minus-min '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [0, 2, 1])

    def test_median_minus_mean(self):
        for v in self.each("(rolling-median-minus-mean '(1 5 3 9 2) 3)"):
            self.assertAlmostEqual(v[0], 3 - 3)
            self.assertAlmostEqual(v[1], 5 - 17 / 3)
            self.assertAlmostEqual(v[2], 3 - 14 / 3)

    def test_mean_minus_median(self):
        for v in self.each("(rolling-mean-minus-median '(1 5 3 9 2) 3)"):
            self.assertAlmostEqual(v[0], 0)
            self.assertAlmostEqual(v[1], 17 / 3 - 5)
            self.assertAlmostEqual(v[2], 14 / 3 - 3)


if __name__ == "__main__":
    unittest.main()
