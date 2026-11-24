"""Phase 114: rolling sum/median/range squared, first cubed."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase114(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (3 6 9) (6 9 12) (9 12 3)
    def test_sum_squared(self):
        for v in self.each("(rolling-sum-squared '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [324, 729, 576])

    def test_median_squared(self):
        for v in self.each("(rolling-median-squared '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [36, 81, 81])

    def test_range_squared(self):
        for v in self.each("(rolling-range-squared '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [36, 36, 81])

    def test_first_cubed(self):
        for v in self.each("(rolling-first-cubed '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [27, 216, 729])


if __name__ == "__main__":
    unittest.main()
