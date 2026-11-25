"""Phase 134: list-interleave, list-chunk, list-windows, list-split-at, list-cartesian, list-transpose."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase134(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_interleave(self):
        self.check("(list-interleave '(1 2 3) '(10 20 30 40 50))", [1, 10, 2, 20, 3, 30, 40, 50])
        self.check("(list-interleave '() '(1))", [1])

    def test_chunk(self):
        self.check("(list-chunk '(1 2 3 4 5 6 7) 3)", [[1, 2, 3], [4, 5, 6], [7]])
        self.check("(list-chunk '() 2)", [])

    def test_windows(self):
        self.check("(list-windows '(1 2 3 4) 2)", [[1, 2], [2, 3], [3, 4]])
        self.check("(list-windows '(1 2) 3)", [])

    def test_split_at(self):
        self.check("(list-split-at '(1 2 3 4 5) 2)", [[1, 2], [3, 4, 5]])
        self.check("(list-split-at '(1 2) 9)", [[1, 2], []])

    def test_cartesian(self):
        self.check("(list-cartesian '(1 2) '(3 4))", [[1, 3], [1, 4], [2, 3], [2, 4]])

    def test_transpose(self):
        self.check("(list-transpose '((1 2 3) (4 5 6)))", [[1, 4], [2, 5], [3, 6]])


if __name__ == "__main__":
    unittest.main()
