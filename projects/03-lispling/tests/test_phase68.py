"""Phase 68: rolling-sum, rolling-max, rolling-min, rolling-range."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase68(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_rolling_sum(self):
        for v in self.each("(rolling-sum '(1 2 3 4 5) 3)"):
            self.assertEqual([int(x) for x in list(v)], [6, 9, 12])

    def test_rolling_sum_short(self):
        for v in self.each("(rolling-sum '(1 2) 3)"):
            self.assertEqual(list(v), [])

    def test_rolling_max_min_range(self):
        for v in self.each("(rolling-max '(1 5 2 4 3) 2)"):
            self.assertEqual([int(x) for x in list(v)], [5, 5, 4, 4])
        for v in self.each("(rolling-min '(4 2 6 1 5) 3)"):
            self.assertEqual([int(x) for x in list(v)], [2, 1, 1])
        for v in self.each("(rolling-range '(1 5 2 8 3) 2)"):
            self.assertEqual([int(x) for x in list(v)], [4, 3, 6, 5])


if __name__ == "__main__":
    unittest.main()
