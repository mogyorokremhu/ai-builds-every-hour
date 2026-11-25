"""Phase 128: generic rolling-<agg>-pow helpers taking an exponent."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))
XS = "'(1 2 3 4 5)"


class TestPhase128(unittest.TestCase):
    def check(self, name, k, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, fn=name, k=k):
                got = [float(x) for x in list(r(f"({name} {XS} 3 {k})"))]
                self.assertEqual(got, [float(e) for e in expected])

    def test_first_last(self):
        self.check("rolling-first-pow", 2, [1, 4, 9])
        self.check("rolling-last-pow", 3, [27, 64, 125])

    def test_max_min(self):
        self.check("rolling-max-pow", 2, [9, 16, 25])
        self.check("rolling-min-pow", 0, [1, 1, 1])

    def test_mean_sum(self):
        self.check("rolling-mean-pow", 4, [16, 81, 256])
        self.check("rolling-sum-pow", 2, [36, 81, 144])

    def test_median_range(self):
        self.check("rolling-median-pow", 3, [8, 27, 64])
        self.check("rolling-range-pow", 10, [2**10] * 3)

    def test_matches_fixed_power(self):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn):
                a = [float(x) for x in list(r(f"(rolling-sum-pow {XS} 2 9)"))]
                b = [float(x) for x in list(r(f"(rolling-sum-ninth {XS} 2)"))]
                self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
