"""Phase 35: list helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase35(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_adjacent_pairs(self):
        self.check("(adjacent-pairs '(1 2 3 4))", [[1, 2], [2, 3], [3, 4]])
        self.check("(adjacent-pairs '(1))", [])

    def test_last_n_drop_last(self):
        self.check("(last-n '(1 2 3 4 5) 2)", [4, 5])
        self.check("(last-n '(1 2) 5)", [1, 2])
        self.check("(drop-last '(1 2 3 4 5) 2)", [1, 2, 3])
        self.check("(drop-last '(1 2) 5)", [])

    def test_argmax(self):
        self.check("(argmax '(3 9 2 9))", 1)
        self.check("(argmax '())", -1)

    def test_running_max(self):
        self.check("(running-max '(1 3 2 5 4))", [1, 3, 3, 5, 5])

    def test_interpose(self):
        self.check("(interpose 0 '(1 2 3))", [1, 0, 2, 0, 3])
        self.check("(interpose 0 '())", [])


if __name__ == "__main__":
    unittest.main()
