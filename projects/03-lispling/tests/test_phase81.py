"""Phase 81: rolling-count-at-least, rolling-count-at-most, rolling-sum-at-most, rolling-sum-equal."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase81(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_count_at_least(self):
        for v in self.each("(rolling-count-at-least 3 '(1 3 5 2 4) 3)"):
            self.assertEqual(v, [2, 2, 2])

    def test_count_at_most(self):
        for v in self.each("(rolling-count-at-most 3 '(1 3 5 2 4) 3)"):
            self.assertEqual(v, [2, 2, 1])

    def test_sum_at_most(self):
        for v in self.each("(rolling-sum-at-most 3 '(1 3 5 2 4) 3)"):
            self.assertEqual(v, [4, 5, 2])

    def test_sum_equal(self):
        for v in self.each("(rolling-sum-equal 2 '(2 3 2 2 4) 3)"):
            self.assertEqual(v, [4, 4, 4])


if __name__ == "__main__":
    unittest.main()
