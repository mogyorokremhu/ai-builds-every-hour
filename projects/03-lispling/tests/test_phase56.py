"""Phase 56: std-dev, covariance, weighted-average, cumulative-max/min."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase56(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_std_dev_cov(self):
        self.check("(std-dev '(2 4 4 4 5 5 7 9))", 2)
        self.check("(covariance '(1 2 3) '(2 4 6))", 4 / 3)

    def test_weighted(self):
        self.check("(weighted-average '(1 2 3) '(1 1 2))", 2.25)

    def test_cumulative_extrema(self):
        self.check("(cumulative-max '(3 1 4 1 5))", [3, 3, 4, 4, 5])
        self.check("(cumulative-min '(3 1 4 1 5))", [3, 1, 1, 1, 1])
        self.check("(cumulative-max '())", [])
