"""Phase 28: constructors, trees, splitting and alist helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase28(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_constructors(self):
        self.check("(make-list 3 'x)", run("(list 'x 'x 'x)"))
        self.check("(list-tabulate 4 (lambda (i) (* i 2)))", [0, 2, 4, 6])
        self.check("(vector-length (vector-tabulate 5 (lambda (i) i)))", 5)
        self.check("(product '(1 2 3 4))", 24)
        self.check("(product '())", 1)

    def test_split(self):
        self.check("(split-at '(1 2 3 4) 1)", [[1], [2, 3, 4]])
        self.check("(span even? '(2 4 5 6))", [[2, 4], [5, 6]])
        self.check("(break even? '(1 3 4 5))", [[1, 3], [4, 5]])

    def test_index_edit(self):
        self.check("(insert-at '(1 3) 1 2)", [1, 2, 3])
        self.check("(delete-at '(1 2 3) 1)", [1, 3])
        self.check("(list-index-of 3 '(1 2 3))", 2)
        self.check("(list-index-of 9 '(1 2 3))", -1)

    def test_trees(self):
        self.check("(tree-leaves '(1 (2 (3 4)) 5))", [1, 2, 3, 4, 5])
        self.check("(tree-depth '(1 (2 (3 4)) 5))", 3)
        self.check("(tree-depth 7)", 0)
        self.check("(tree-map (lambda (x) (+ x 1)) '(1 (2 3)))", [2, [3, 4]])

    def test_alists(self):
        self.check("(alist-keys '((a . 1) (b . 2)))", run("(list 'a 'b)"))
        self.check("(alist-values '((a . 1) (b . 2)))", [1, 2])
        self.check("(hash-ref (alist->hash '((a . 1))) 'a)", 1)


if __name__ == "__main__":
    unittest.main()
