"""Phase 94: rolling first+last, max+min, mean/median vs sum."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase94(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_first_plus_last(self):
        for v in self.each("(rolling-first-plus-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [12, 18, 12])

    def test_max_plus_min(self):
        for v in self.each("(rolling-max-plus-min '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [12, 18, 15])

    def test_mean_minus_sum(self):
        for v in self.each("(rolling-mean-minus-sum '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [-12, -18, -16])

    def test_median_minus_sum(self):
        for v in self.each("(rolling-median-minus-sum '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [-12, -18, -15])


if __name__ == "__main__":
    unittest.main()
