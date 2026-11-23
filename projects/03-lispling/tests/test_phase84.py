"""Phase 84: rolling-count/sum-at-most-mean, rolling-count/sum-equal-mean."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase84(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_count_at_most_mean(self):
        for v in self.each("(rolling-count-at-most-mean '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [2, 2, 2])

    def test_sum_at_most_mean(self):
        for v in self.each("(rolling-sum-at-most-mean '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [4, 8, 5])

    def test_count_equal_mean(self):
        for v in self.each("(rolling-count-equal-mean '(2 2 2 9 2) 3)"):
            self.assertEqual(v, [3, 0, 0])

    def test_sum_equal_mean(self):
        for v in self.each("(rolling-sum-equal-mean '(2 2 2 9 2) 3)"):
            self.assertEqual(v, [6, 0, 0])


if __name__ == "__main__":
    unittest.main()
