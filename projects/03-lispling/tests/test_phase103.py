"""Phase 103: rolling sum*first, sum*last, mean*first, mean*last."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase103(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_sum_times_first(self):
        for v in self.each("(rolling-sum-times-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 162, 216])

    def test_sum_times_last(self):
        for v in self.each("(rolling-sum-times-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [162, 324, 72])

    def test_mean_times_first(self):
        for v in self.each("(rolling-mean-times-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 54, 72])

    def test_mean_times_last(self):
        for v in self.each("(rolling-mean-times-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [54, 108, 24])


if __name__ == "__main__":
    unittest.main()
