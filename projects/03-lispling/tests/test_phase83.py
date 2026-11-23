"""Phase 83: rolling-count-below-mean, rolling-sum-below-mean, rolling-count-at-least-mean, rolling-sum-at-least-mean."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase83(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_count_below_mean(self):
        for v in self.each("(rolling-count-below-mean '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [1, 2, 2])

    def test_sum_below_mean(self):
        for v in self.each("(rolling-sum-below-mean '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [1, 8, 5])

    def test_count_at_least_mean(self):
        for v in self.each("(rolling-count-at-least-mean '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [2, 1, 1])

    def test_sum_at_least_mean(self):
        for v in self.each("(rolling-sum-at-least-mean '(2 2 2 9 2) 3)"):
            self.assertEqual(v, [6, 9, 9])


if __name__ == "__main__":
    unittest.main()
