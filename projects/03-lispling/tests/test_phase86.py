"""Phase 86: rolling last/first vs mean, max-vs-last, last-vs-min gaps."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase86(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_last_minus_mean(self):
        for v in self.each("(rolling-last-minus-mean '(1 5 3 9 2) 3)"):
            self.assertAlmostEqual(v[0], 3 - 3)
            self.assertAlmostEqual(v[1], 9 - 17 / 3)
            self.assertAlmostEqual(v[2], 2 - 14 / 3)

    def test_first_minus_mean(self):
        for v in self.each("(rolling-first-minus-mean '(1 5 3 9 2) 3)"):
            self.assertAlmostEqual(v[0], 1 - 3)
            self.assertAlmostEqual(v[1], 5 - 17 / 3)
            self.assertAlmostEqual(v[2], 3 - 14 / 3)

    def test_max_minus_last(self):
        for v in self.each("(rolling-max-minus-last '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [2, 0, 7])

    def test_last_minus_min(self):
        for v in self.each("(rolling-last-minus-min '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [2, 6, 0])


if __name__ == "__main__":
    unittest.main()
