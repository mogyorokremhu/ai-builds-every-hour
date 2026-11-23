"""Phase 78: rolling-count-below, rolling-sum-below, rolling-count-between, rolling-sum-above."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase78(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_count_below(self):
        for v in self.each("(rolling-count-below 3 '(1 3 5 2 4) 3)"):
            self.assertEqual(v, [1, 1, 1])

    def test_sum_below(self):
        for v in self.each("(rolling-sum-below 4 '(1 3 5 2 4) 2)"):
            self.assertEqual(v, [4, 3, 2, 2])

    def test_count_between(self):
        for v in self.each("(rolling-count-between 2 4 '(1 3 5 2 4) 3)"):
            self.assertEqual(v, [1, 2, 2])

    def test_sum_above(self):
        for v in self.each("(rolling-sum-above 2 '(1 3 5 2 4) 3)"):
            self.assertEqual(v, [8, 8, 9])


if __name__ == "__main__":
    unittest.main()
