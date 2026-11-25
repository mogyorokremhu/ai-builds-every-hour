"""Phase 133: list-rotate, list-adjacent-pairs, list-dedupe-runs, list-run-lengths."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase133(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_rotate(self):
        self.check("(list-rotate '(1 2 3 4 5) 2)", [3, 4, 5, 1, 2])
        self.check("(list-rotate '(1 2 3) 7)", [2, 3, 1])
        self.check("(list-rotate '(1 2 3) -1)", [3, 1, 2])
        self.check("(list-rotate '() 3)", [])

    def test_pairs(self):
        self.check("(list-adjacent-pairs '(1 2 3 4))", [[1, 2], [2, 3], [3, 4]])
        self.check("(list-adjacent-pairs '(1))", [])

    def test_dedupe(self):
        self.check("(list-dedupe-runs '(1 1 2 2 2 3 1 1))", [1, 2, 3, 1])

    def test_run_lengths(self):
        self.check("(list-run-lengths '(1 1 2 3 3 3))", [[1, 2], [2, 1], [3, 3]])
        self.check("(list-run-lengths '())", [])


if __name__ == "__main__":
    unittest.main()
