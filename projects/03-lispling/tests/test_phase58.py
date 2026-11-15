"""Phase 58: percentile, interquartile-range, ranks, normalize-sum."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase58(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield r(src)

    def test_percentile(self):
        for v in self.each("(percentile '(5 1 4 2 3) 0.5)"):
            self.assertEqual(v, 3)
        for v in self.each("(percentile '(5 1 4 2 3) 1)"):
            self.assertEqual(v, 5)

    def test_iqr(self):
        for v in self.each("(interquartile-range '(1 2 3 4 5 6 7 8 9))"):
            self.assertEqual(v, 4)

    def test_ranks(self):
        for v in self.each("(ranks '(30 10 20))"):
            self.assertEqual(list(v), [3, 1, 2])

    def test_normalize_sum(self):
        for v in self.each("(normalize-sum '(1 1 2))"):
            self.assertEqual([float(x) for x in v], [0.25, 0.25, 0.5])


if __name__ == "__main__":
    unittest.main()
