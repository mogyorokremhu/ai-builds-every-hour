"""Phase 141: list-running-min, list-spread, list-count-distinct, list-replace-all, list-take-last-while."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase141(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_running_min(self):
        self.check("(list-running-min '(5 3 4 1 2))", [5, 3, 3, 1, 1])
        self.check("(list-running-min '())", [])

    def test_spread(self):
        self.check("(list-spread '(4 9 2 7))", 7)

    def test_count_distinct(self):
        self.check("(list-count-distinct '(1 2 2 3 3 3))", 3)

    def test_replace_all(self):
        self.check("(list-replace-all 2 9 '(1 2 3 2))", [1, 9, 3, 9])

    def test_take_last_while(self):
        self.check("(list-take-last-while odd? '(2 4 5 7))", [5, 7])
        self.check("(list-take-last-while odd? '(2 4))", [])


if __name__ == "__main__":
    unittest.main()
