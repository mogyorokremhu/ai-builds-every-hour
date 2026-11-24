"""Phase 106: rolling first*max, first*min, last*max, last*min."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase106(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_first_times_max(self):
        for v in self.each("(rolling-first-times-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [27, 72, 108])

    def test_first_times_min(self):
        for v in self.each("(rolling-first-times-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 36, 27])

    def test_last_times_max(self):
        for v in self.each("(rolling-last-times-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [81, 144, 36])

    def test_last_times_min(self):
        for v in self.each("(rolling-last-times-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [27, 72, 9])


if __name__ == "__main__":
    unittest.main()
