"""Phase 25: variadic curry/partial and function combinators."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestCombinators(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_curry_old_style(self):
        self.check("((curry + 1) 2)", 3)

    def test_curry_many_args(self):
        self.check("((curry list 1 2) 3 4)", [1, 2, 3, 4])
        self.check("((curry list))", [])

    def test_partial_alias(self):
        self.check("(map (partial * 2) '(1 2 3))", [2, 4, 6])

    def test_constantly(self):
        self.check("((constantly 7) 1 2 3)", 7)

    def test_complement(self):
        self.check("(filter (complement even?) '(1 2 3 4 5))", [1, 3, 5])

    def test_juxt(self):
        self.check("((juxt car cdr length) '(1 2 3))", [1, [2, 3], 3])

    def test_compose_star(self):
        self.check("((compose* square (curry + 1)) 4)", 25)
        self.check("((compose* (curry + 1) (curry * 2) +) 1 2)", 7)
        self.check("((compose*) 5)", 5)


if __name__ == "__main__":
    unittest.main()
