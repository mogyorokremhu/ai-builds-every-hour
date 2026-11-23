"""Phase 89: rolling median vs max/min/first/last gaps."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))
# windows of '(1 5 3 9 2) size 3: (1 5 3) (5 3 9) (3 9 2); medians 3, 5, 3


class TestPhase89(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_max_minus_median(self):
        for v in self.each("(rolling-max-minus-median '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [2, 4, 6])

    def test_median_minus_min(self):
        for v in self.each("(rolling-median-minus-min '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [2, 2, 1])

    def test_median_minus_first(self):
        for v in self.each("(rolling-median-minus-first '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [2, 0, 0])

    def test_last_minus_median(self):
        for v in self.each("(rolling-last-minus-median '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [0, 4, -1])


if __name__ == "__main__":
    unittest.main()
