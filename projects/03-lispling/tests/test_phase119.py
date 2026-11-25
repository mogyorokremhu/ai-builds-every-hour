"""Phase 119: rolling first/last/max/min to the fifth power."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase119(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (3 6 9) (6 9 12) (9 12 3)
    def test_first_fifth(self):
        for v in self.each("(rolling-first-fifth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [243, 7776, 59049])

    def test_last_fifth(self):
        for v in self.each("(rolling-last-fifth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [59049, 248832, 243])

    def test_max_fifth(self):
        for v in self.each("(rolling-max-fifth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [59049, 248832, 248832])

    def test_min_fifth(self):
        for v in self.each("(rolling-min-fifth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [243, 7776, 243])


if __name__ == "__main__":
    unittest.main()
