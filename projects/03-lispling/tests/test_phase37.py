"""Phase 37: list helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase37(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_differences(self):
        self.check("(differences '(1 4 9 16))", [3, 5, 7])
        self.check("(differences '(5))", [])

    def test_take_last(self):
        self.check("(take-last '(1 2 3 4) 2)", [3, 4])
        self.check("(take-last '(1 2) 5)", [1, 2])
        self.check("(take-last '(1 2) 0)", [])

    def test_split_on(self):
        self.check("(split-on 0 '(1 2 0 3 0 0 4))", [[1, 2], [3], [], [4]])
        self.check("(split-on 0 '())", [[]])

    def test_min_max_list(self):
        self.check("(min-max-list '(3 9 -2 5))", [-2, 9])

    def test_flatten_once(self):
        self.check("(flatten-once '((1 2) (3) () ((4))))", [1, 2, 3, [4]])

    def test_zip3(self):
        self.check("(zip3 '(1 2 3) '(a b) '(x y z))", [[1, "a", "x"], [2, "b", "y"]])


if __name__ == "__main__":
    unittest.main()
