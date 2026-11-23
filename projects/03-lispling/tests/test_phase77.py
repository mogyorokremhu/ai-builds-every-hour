"""Phase 77: rolling-count-zero, rolling-sum-cubes, rolling-product-abs, rolling-count-above."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase77(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_count_zero(self):
        for v in self.each("(rolling-count-zero '(0 1 0 0 2) 2)"):
            self.assertEqual(v, [1, 1, 2, 1])

    def test_sum_cubes(self):
        for v in self.each("(rolling-sum-cubes '(1 2 3 4) 2)"):
            self.assertEqual(v, [9, 35, 91])

    def test_product_abs(self):
        for v in self.each("(rolling-product-abs '(-2 3 -4 5) 2)"):
            self.assertEqual(v, [6, 12, 20])

    def test_count_above(self):
        for v in self.each("(rolling-count-above 2 '(1 3 5 2 4) 3)"):
            self.assertEqual(v, [2, 2, 2])


if __name__ == "__main__":
    unittest.main()
