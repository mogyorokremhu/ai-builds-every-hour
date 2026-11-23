"""Phase 88: rolling last vs first, mean vs max, min vs mean gaps."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase88(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_last_minus_first(self):
        for v in self.each("(rolling-last-minus-first '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [2, 4, -1])

    def test_first_minus_last(self):
        for v in self.each("(rolling-first-minus-last '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [-2, -4, 1])

    def test_mean_minus_max(self):
        for v in self.each("(rolling-mean-minus-max '(1 5 3 9 2) 3)"):
            self.assertAlmostEqual(v[0], 3 - 5)
            self.assertAlmostEqual(v[1], 17 / 3 - 9)
            self.assertAlmostEqual(v[2], 14 / 3 - 9)

    def test_min_minus_mean(self):
        for v in self.each("(rolling-min-minus-mean '(1 5 3 9 2) 3)"):
            self.assertAlmostEqual(v[0], 1 - 3)
            self.assertAlmostEqual(v[1], 3 - 17 / 3)
            self.assertAlmostEqual(v[2], 2 - 14 / 3)


if __name__ == "__main__":
    unittest.main()
