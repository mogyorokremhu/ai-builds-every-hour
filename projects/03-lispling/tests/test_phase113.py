"""Phase 113: rolling first/last/max/min squared."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase113(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (3 6 9) (6 9 12) (9 12 3)
    def test_first_squared(self):
        for v in self.each("(rolling-first-squared '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 36, 81])

    def test_last_squared(self):
        for v in self.each("(rolling-last-squared '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [81, 144, 9])

    def test_max_squared(self):
        for v in self.each("(rolling-max-squared '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [81, 144, 144])

    def test_min_squared(self):
        for v in self.each("(rolling-min-squared '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [9, 36, 9])


if __name__ == "__main__":
    unittest.main()
