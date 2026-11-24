"""Phase 95: rolling first+max, last+min, sum+max, sum+min."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase95(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_first_plus_max(self):
        for v in self.each("(rolling-first-plus-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [12, 18, 21])

    def test_last_plus_min(self):
        for v in self.each("(rolling-last-plus-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [12, 18, 6])

    def test_sum_plus_max(self):
        for v in self.each("(rolling-sum-plus-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [27, 39, 36])

    def test_sum_plus_min(self):
        for v in self.each("(rolling-sum-plus-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [21, 33, 27])


if __name__ == "__main__":
    unittest.main()
