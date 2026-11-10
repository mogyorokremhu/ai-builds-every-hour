"""Phase 27: set operations, combinatorics and vector utilities."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase27(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_sets(self):
        self.check("(list-union '(1 2 3) '(3 4 4 5))", [1, 2, 3, 4, 5])
        self.check("(list-intersection '(1 2 3 3) '(3 2 9))", [2, 3])
        self.check("(list-difference '(1 2 3 4) '(2 4))", [1, 3])
        self.check("(subset? '(1 2) '(3 2 1))", True)
        self.check("(subset? '(1 5) '(3 2 1))", False)

    def test_take_drop_right(self):
        self.check("(take-right '(1 2 3 4 5) 2)", [4, 5])
        self.check("(drop-right '(1 2 3 4 5) 2)", [1, 2, 3])

    def test_rotate(self):
        self.check("(rotate '(1 2 3 4) 1)", [2, 3, 4, 1])
        self.check("(rotate '(1 2 3 4) -1)", [4, 1, 2, 3])
        self.check("(rotate '() 3)", [])

    def test_pairwise(self):
        self.check("(pairwise '(1 2 3))", [[1, 2], [2, 3]])
        self.check("(pairwise '(1))", [])

    def test_product_and_power_set(self):
        self.check("(cartesian-product '(1 2) '(a b))",
                   [[1, "a"], [1, "b"], [2, "a"], [2, "b"]])
        self.check("(length (power-set '(1 2 3 4)))", 16)

    def test_combinations_permutations(self):
        self.check("(combinations '(1 2 3) 2)", [[1, 2], [1, 3], [2, 3]])
        self.check("(length (permutations '(1 2 3 4)))", 24)
        self.check("(permutations '(1 2))", [[1, 2], [2, 1]])

    def test_vectors(self):
        self.check("(vector->list (subvector (vector 1 2 3 4 5) 1 4))", [2, 3, 4])
        self.check("(vector->list (vector-append (vector 1) (vector 2 3)))", [1, 2, 3])
        self.check("(vector->list (vector-reverse (vector 1 2 3)))", [3, 2, 1])
        self.check("(vector-count even? (vector 1 2 4 5))", 2)
        self.check("(vector-index even? (vector 1 3 4))", 2)
        self.check("(vector-index even? (vector 1 3))", False)

    def test_binary_search(self):
        self.check("(vector-binary-search (vector 1 3 5 7 9) 7)", 3)
        self.check("(vector-binary-search (vector 1 3 5 7 9) 4)", False)


if __name__ == "__main__":
    unittest.main()
