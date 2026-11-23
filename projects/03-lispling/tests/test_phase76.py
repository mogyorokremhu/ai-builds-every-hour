"""Phase 76: rolling-sum-odds, rolling-min-abs, rolling-count-evens, rolling-count-odds."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase76(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_sum_odds(self):
        for v in self.each("(rolling-sum-odds '(1 2 3 5 6) 2)"):
            self.assertEqual(v, [1, 3, 8, 5])

    def test_min_abs(self):
        for v in self.each("(rolling-min-abs '(-5 2 -3 4) 2)"):
            self.assertEqual(v, [2, 2, 3])

    def test_count_evens(self):
        for v in self.each("(rolling-count-evens '(1 2 4 5 6) 2)"):
            self.assertEqual(v, [1, 2, 1, 1])

    def test_count_odds(self):
        for v in self.each("(rolling-count-odds '(1 2 4 5 6) 2)"):
            self.assertEqual(v, [1, 0, 1, 1])


if __name__ == "__main__":
    unittest.main()
