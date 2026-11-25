"""Phase 135: list-insert-at, list-remove-at, list-intersperse, list-subsets, list-combinations, list-permutations."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase135(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_insert_remove(self):
        self.check("(list-insert-at '(1 2 4) 2 3)", [1, 2, 3, 4])
        self.check("(list-insert-at '(1) 9 2)", [1, 2])
        self.check("(list-remove-at '(1 2 3 4) 1)", [1, 3, 4])
        self.check("(list-remove-at '(1 2) 5)", [1, 2])

    def test_intersperse(self):
        self.check("(list-intersperse '(1 2 3) 0)", [1, 0, 2, 0, 3])
        self.check("(list-intersperse '() 0)", [])
        self.check("(list-intersperse '(7) 0)", [7])

    def test_subsets(self):
        self.check("(length (list-subsets '(1 2 3 4)))", 16)
        self.check("(list-subsets '())", [[]])

    def test_combinations(self):
        self.check("(list-combinations '(1 2 3 4) 2)",
                   [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]])
        self.check("(list-combinations '(1 2) 3)", [])

    def test_permutations(self):
        self.check("(list-permutations '(1 2 3))",
                   [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
        self.check("(length (list-permutations '(1 2 3 4)))", 24)


if __name__ == "__main__":
    unittest.main()
