"""Phase 105: rolling min*first, min*last, range*first, range*last."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase105(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_min_times_first(self):
        for v in self.each("(rolling-min-times-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 36, 27])

    def test_min_times_last(self):
        for v in self.each("(rolling-min-times-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [27, 72, 9])

    def test_range_times_first(self):
        for v in self.each("(rolling-range-times-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 36, 81])

    def test_range_times_last(self):
        for v in self.each("(rolling-range-times-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 72, 27])


if __name__ == "__main__":
    unittest.main()
