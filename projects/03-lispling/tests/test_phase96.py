"""Phase 96: rolling first+min, last+max, median+max, median+min."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase96(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_first_plus_min(self):
        for v in self.each("(rolling-first-plus-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [6, 12, 12])

    def test_last_plus_max(self):
        for v in self.each("(rolling-last-plus-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 24, 15])

    def test_median_plus_max(self):
        for v in self.each("(rolling-median-plus-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [15, 21, 21])

    def test_median_plus_min(self):
        for v in self.each("(rolling-median-plus-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 15, 12])


if __name__ == "__main__":
    unittest.main()
