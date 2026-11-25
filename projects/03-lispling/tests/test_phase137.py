"""Phase 137: list-last, list-count-if, list-zip-with, list-partition, list-unique, list-drop-last."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase137(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_last(self):
        self.check("(list-last '(1 2 3))", 3)
        self.check("(list-last '())", False)

    def test_count_if(self):
        self.check("(list-count-if even? '(1 2 3 4 6))", 3)
        self.check("(list-count-if even? '())", 0)

    def test_zip_with(self):
        self.check("(list-zip-with + '(1 2 3) '(10 20))", [11, 22])

    def test_partition(self):
        self.check("(list-partition even? '(1 2 3 4))", [[2, 4], [1, 3]])

    def test_unique(self):
        self.check("(list-unique '(1 2 1 3 2))", [1, 2, 3])

    def test_drop_last(self):
        self.check("(list-drop-last '(1 2 3 4) 2)", [1, 2])
        self.check("(list-drop-last '(1 2) 5)", [])


if __name__ == "__main__":
    unittest.main()
