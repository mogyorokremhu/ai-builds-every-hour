"""Phase 140: list-span, list-group-by, list-count-by, list-take-last, list-running-max."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase140(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_span(self):
        self.check("(list-span even? '(2 4 5 6))", [[2, 4], [5, 6]])

    def test_group_by(self):
        self.check("(map cdr (list-group-by even? '(1 2 3 4 5)))", [[1, 3, 5], [2, 4]])

    def test_count_by(self):
        self.check("(map cdr (list-count-by even? '(1 2 3 4 5)))", [3, 2])

    def test_take_last(self):
        self.check("(list-take-last 2 '(1 2 3 4))", [3, 4])
        self.check("(list-take-last 9 '(1 2))", [1, 2])

    def test_running_max(self):
        self.check("(list-running-max '(1 3 2 5 4))", [1, 3, 3, 5, 5])
        self.check("(list-running-max '())", [])


if __name__ == "__main__":
    unittest.main()
