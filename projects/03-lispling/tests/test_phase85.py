"""Phase 85: rolling not-equal-mean helpers and max/min vs mean gaps."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase85(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_count_not_equal_mean(self):
        for v in self.each("(rolling-count-not-equal-mean '(2 2 2 9 2) 3)"):
            self.assertEqual(v, [0, 3, 3])

    def test_sum_not_equal_mean(self):
        for v in self.each("(rolling-sum-not-equal-mean '(2 2 2 9 2) 3)"):
            self.assertEqual(v, [0, 13, 13])

    def test_max_minus_mean(self):
        for v in self.each("(rolling-max-minus-mean '(1 5 3 9 2) 3)"):
            self.assertAlmostEqual(v[0], 5 - 3)
            self.assertAlmostEqual(v[1], 9 - 17 / 3)
            self.assertAlmostEqual(v[2], 9 - 14 / 3)

    def test_mean_minus_min(self):
        for v in self.each("(rolling-mean-minus-min '(1 5 3 9 2) 3)"):
            self.assertAlmostEqual(v[0], 3 - 1)
            self.assertAlmostEqual(v[1], 17 / 3 - 3)
            self.assertAlmostEqual(v[2], 14 / 3 - 2)


if __name__ == "__main__":
    unittest.main()
