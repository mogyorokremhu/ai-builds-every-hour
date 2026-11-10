"""Phase 34: list helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase34(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_rotate(self):
        self.check("(rotate-left '(1 2 3 4 5) 2)", [3, 4, 5, 1, 2])
        self.check("(rotate-right '(1 2 3 4 5) 1)", [5, 1, 2, 3, 4])
        self.check("(rotate-left '() 3)", [])
        self.check("(rotate-left '(1 2 3) 5)", [3, 1, 2])

    def test_index(self):
        self.check("(index-of '(a b c b) 'b)", 1)
        self.check("(last-index-of '(a b c b) 'b)", 3)
        self.check("(index-of '(a) 'z)", -1)

    def test_zip_with(self):
        self.check("(zip-with + '(1 2 3) '(10 20))", [11, 22])

    def test_range_step(self):
        self.check("(range-step 0 10 3)", [0, 3, 6, 9])
        self.check("(range-step 10 0 -3)", [10, 7, 4, 1])

    def test_flatten_depth(self):
        self.check("(flatten-depth '(1 (2 (3))) 1)", [1, 2, [3]])
        self.check("(flatten-depth '(1 (2 (3))) 2)", [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
