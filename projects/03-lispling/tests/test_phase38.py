"""Phase 38: list helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase38(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_count_if(self):
        self.check("(count-if even? '(1 2 3 4 6))", 3)

    def test_list_index_if(self):
        self.check("(list-index-if (lambda (x) (> x 2)) '(1 2 3 4))", 2)
        self.check("(list-index-if (lambda (x) (> x 9)) '(1 2))", -1)

    def test_remove_if(self):
        self.check("(remove-if even? '(1 2 3 4 5))", [1, 3, 5])

    def test_sum_list(self):
        self.check("(sum-list '(1 2 3 4))", 10)

    def test_cartesian(self):
        self.check("(cartesian '(1 2) '(a b))", [[1, "a"], [1, "b"], [2, "a"], [2, "b"]])

    def test_map_pairs(self):
        self.check("(map-pairs + '(1 2 3 4))", [3, 5, 7])


if __name__ == "__main__":
    unittest.main()
