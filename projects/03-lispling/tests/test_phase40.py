"""Phase 40: list helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase40(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_list_max_by(self):
        self.check("(list-max-by abs '(1 -5 3))", -5)

    def test_count_occurrences(self):
        self.check("(count-occurrences 2 '(1 2 2 3 2))", 3)

    def test_pairwise(self):
        self.check("(pairwise + '(1 2 3 4))", [3, 5, 7])
        self.check("(pairwise + '(1))", [])

    def test_mean_of_squares(self):
        self.check("(mean-of-squares '(3 3))", 9)

    def test_take_nth(self):
        self.check("(take-nth 2 '(1 2 3 4 5))", [1, 3, 5])
        self.check("(take-nth 3 '())", [])

    def test_take_nth_tail(self):
        self.check("(list-tail-safe '(1 2 3) 5)", [])


if __name__ == "__main__":
    unittest.main()
