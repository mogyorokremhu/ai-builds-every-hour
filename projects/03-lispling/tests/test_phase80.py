"""Phase 80: rolling-count-not-equal, rolling-sum-outside, rolling-count-nonmultiples, rolling-sum-multiples."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase80(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_count_not_equal(self):
        for v in self.each("(rolling-count-not-equal 2 '(2 3 2 2 4) 3)"):
            self.assertEqual(v, [1, 1, 1])

    def test_sum_outside(self):
        for v in self.each("(rolling-sum-outside 2 4 '(1 3 5 2 4) 3)"):
            self.assertEqual(v, [6, 5, 5])

    def test_count_nonmultiples(self):
        for v in self.each("(rolling-count-nonmultiples 2 '(1 2 4 5 6) 3)"):
            self.assertEqual(v, [1, 1, 1])

    def test_sum_multiples(self):
        for v in self.each("(rolling-sum-multiples 2 '(1 2 4 5 6) 3)"):
            self.assertEqual(v, [6, 6, 10])


if __name__ == "__main__":
    unittest.main()
