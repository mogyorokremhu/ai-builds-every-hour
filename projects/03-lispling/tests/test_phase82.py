"""Phase 82: rolling-sum-not-equal, rolling-sum-nonmultiples, rolling-count-above-mean, rolling-sum-above-mean."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase82(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_sum_not_equal(self):
        for v in self.each("(rolling-sum-not-equal 2 '(2 3 2 2 4) 3)"):
            self.assertEqual(v, [3, 3, 4])

    def test_sum_nonmultiples(self):
        for v in self.each("(rolling-sum-nonmultiples 2 '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [4, 3, 8])

    def test_count_above_mean(self):
        for v in self.each("(rolling-count-above-mean '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [1, 1, 1])

    def test_sum_above_mean(self):
        for v in self.each("(rolling-sum-above-mean '(1 5 3 9 2) 3)"):
            self.assertEqual(v, [5, 9, 9])


if __name__ == "__main__":
    unittest.main()
