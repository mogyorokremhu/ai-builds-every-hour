"""Phase 104: rolling median*first, median*last, max*first, max*last."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase104(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_median_times_first(self):
        for v in self.each("(rolling-median-times-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 54, 81])

    def test_median_times_last(self):
        for v in self.each("(rolling-median-times-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 108, 27])

    def test_max_times_first(self):
        for v in self.each("(rolling-max-times-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [27, 72, 108])

    def test_max_times_last(self):
        for v in self.each("(rolling-max-times-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [81, 144, 36])


if __name__ == "__main__":
    unittest.main()
