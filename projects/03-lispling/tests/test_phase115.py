"""Phase 115: rolling mean/last/max/min cubed."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase115(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (3 6 9) (6 9 12) (9 12 3)
    def test_mean_cubed(self):
        for v in self.each("(rolling-mean-cubed '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [216, 729, 512])

    def test_last_cubed(self):
        for v in self.each("(rolling-last-cubed '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [729, 1728, 27])

    def test_max_cubed(self):
        for v in self.each("(rolling-max-cubed '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [729, 1728, 1728])

    def test_min_cubed(self):
        for v in self.each("(rolling-min-cubed '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [27, 216, 27])


if __name__ == "__main__":
    unittest.main()
