"""Phase 75: rolling-count-positive, rolling-count-negative, rolling-max-abs, rolling-sum-evens."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase75(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_count_positive(self):
        for v in self.each("(rolling-count-positive '(-1 2 -3 4) 2)"):
            self.assertEqual(v, [1, 1, 1])

    def test_count_negative(self):
        for v in self.each("(rolling-count-negative '(-1 -2 3 -4) 2)"):
            self.assertEqual(v, [2, 1, 1])

    def test_max_abs(self):
        for v in self.each("(rolling-max-abs '(-5 2 -3 4) 2)"):
            self.assertEqual(v, [5, 3, 4])

    def test_sum_evens(self):
        for v in self.each("(rolling-sum-evens '(1 2 4 5 6) 2)"):
            self.assertEqual(v, [2, 6, 4, 6])


if __name__ == "__main__":
    unittest.main()
