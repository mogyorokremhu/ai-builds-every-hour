"""Phase 39: list helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase39(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_list_set(self):
        self.check("(list-set '(1 2 3) 1 'x)", [1, "x", 3])

    def test_member_if(self):
        self.check("(member-if even? '(1 3 4 5))", [4, 5])
        self.check("(member-if even? '(1 3))", False)

    def test_subsequence(self):
        self.check("(subsequence? '(1 3) '(1 2 3 4))", True)
        self.check("(subsequence? '(3 1) '(1 2 3 4))", False)

    def test_all_pairs(self):
        self.check("(all-pairs '(1 2 3))", [[1, 2], [1, 3], [2, 3]])

    def test_sum_of_squares(self):
        self.check("(sum-of-squares '(1 2 3))", 14)

    def test_dedupe_by(self):
        self.check("(dedupe-by (lambda (x) (modulo x 3)) '(1 2 3 4 5 6))", [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
