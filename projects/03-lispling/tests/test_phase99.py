"""Phase 99: rolling sum+first, sum+last, sum+mean, range+mean."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase99(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_sum_plus_first(self):
        for v in self.each("(rolling-sum-plus-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [21, 33, 33])

    def test_sum_plus_last(self):
        for v in self.each("(rolling-sum-plus-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [27, 39, 27])

    def test_sum_plus_mean(self):
        for v in self.each("(rolling-sum-plus-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [24, 36, 32])

    def test_range_plus_mean(self):
        for v in self.each("(rolling-range-plus-mean '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [12, 15, 17])


if __name__ == "__main__":
    unittest.main()
