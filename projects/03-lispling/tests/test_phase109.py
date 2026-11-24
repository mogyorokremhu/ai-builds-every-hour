"""Phase 109: rolling first*median, last*median, first*range, last*range."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase109(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_first_times_median(self):
        # windows (3 6 9) (6 9 12) (9 12 3): medians 6, 9, 9
        for v in self.each("(rolling-first-times-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 54, 81])

    def test_last_times_median(self):
        for v in self.each("(rolling-last-times-median '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 108, 27])

    def test_first_times_range(self):
        # ranges 6, 6, 9
        for v in self.each("(rolling-first-times-range '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 36, 81])

    def test_last_times_range(self):
        for v in self.each("(rolling-last-times-range '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 72, 27])


if __name__ == "__main__":
    unittest.main()
