"""Phase 73: rolling-first, rolling-last, rolling-sum-abs, rolling-mean-abs."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase73(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_first(self):
        for v in self.each("(rolling-first '(1 2 3 4) 2)"):
            self.assertEqual(v, [1, 2, 3])

    def test_last(self):
        for v in self.each("(rolling-last '(1 2 3 4) 2)"):
            self.assertEqual(v, [2, 3, 4])

    def test_sum_abs(self):
        for v in self.each("(rolling-sum-abs '(-1 2 -3 4) 2)"):
            self.assertEqual(v, [3, 5, 7])

    def test_mean_abs(self):
        for v in self.each("(rolling-mean-abs '(-1 2 -3 4) 2)"):
            self.assertEqual(v, [1.5, 2.5, 3.5])


if __name__ == "__main__":
    unittest.main()
