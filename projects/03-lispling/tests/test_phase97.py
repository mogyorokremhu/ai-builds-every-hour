"""Phase 97: rolling first+median, last+median, mean+max, mean+min."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase97(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_first_plus_median(self):
        for v in self.each("(rolling-first-plus-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 15, 18])

    def test_last_plus_median(self):
        for v in self.each("(rolling-last-plus-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [15, 21, 12])

    def test_mean_plus_max(self):
        for v in self.each("(rolling-mean-plus-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [15, 21, 20])

    def test_mean_plus_min(self):
        for v in self.each("(rolling-mean-plus-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 15, 11])


if __name__ == "__main__":
    unittest.main()
