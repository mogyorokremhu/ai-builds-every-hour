"""Phase 101: rolling median+first, median+last, range+first, range+last."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase101(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_median_plus_first(self):
        for v in self.each("(rolling-median-plus-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 15, 18])

    def test_median_plus_last(self):
        for v in self.each("(rolling-median-plus-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [15, 21, 12])

    def test_range_plus_first(self):
        for v in self.each("(rolling-range-plus-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 12, 18])

    def test_range_plus_last(self):
        for v in self.each("(rolling-range-plus-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [15, 18, 12])


if __name__ == "__main__":
    unittest.main()
