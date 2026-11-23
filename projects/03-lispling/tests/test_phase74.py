"""Phase 74: rolling-count-nonzero, rolling-sum-positive, rolling-sum-negative, rolling-spread."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase74(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_count_nonzero(self):
        for v in self.each("(rolling-count-nonzero '(0 1 0 2 3) 2)"):
            self.assertEqual(v, [1, 1, 1, 2])

    def test_sum_positive(self):
        for v in self.each("(rolling-sum-positive '(-1 2 -3 4) 2)"):
            self.assertEqual(v, [2, 2, 4])

    def test_sum_negative(self):
        for v in self.each("(rolling-sum-negative '(-1 2 -3 4) 2)"):
            self.assertEqual(v, [-1, -3, -3])

    def test_spread(self):
        for v in self.each("(rolling-spread '(1 5 2 8) 2)"):
            self.assertEqual(v, [4, 3, 6])


if __name__ == "__main__":
    unittest.main()
