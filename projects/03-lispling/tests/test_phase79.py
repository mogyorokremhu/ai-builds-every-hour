"""Phase 79: rolling-sum-between, rolling-count-equal, rolling-count-outside, rolling-count-multiples."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase79(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_sum_between(self):
        for v in self.each("(rolling-sum-between 2 4 '(1 3 5 2 4) 3)"):
            self.assertEqual(v, [3, 5, 6])

    def test_count_equal(self):
        for v in self.each("(rolling-count-equal 2 '(2 3 2 2 4) 3)"):
            self.assertEqual(v, [2, 2, 2])

    def test_count_outside(self):
        for v in self.each("(rolling-count-outside 2 4 '(1 3 5 2 4) 3)"):
            self.assertEqual(v, [2, 1, 1])

    def test_count_multiples(self):
        for v in self.each("(rolling-count-multiples 2 '(1 2 4 5 6) 3)"):
            self.assertEqual(v, [2, 2, 2])


if __name__ == "__main__":
    unittest.main()
