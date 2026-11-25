"""Phase 136: list-scan, list-take-every, list-flatten-once, list-argmax, list-argmin."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase136(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_scan(self):
        self.check("(list-scan + 0 '(1 2 3 4))", [0, 1, 3, 6, 10])
        self.check("(list-scan * 1 '())", [1])

    def test_take_every(self):
        self.check("(list-take-every '(1 2 3 4 5 6 7) 3)", [1, 4, 7])
        self.check("(list-take-every '() 2)", [])
        self.check("(list-take-every '(1 2 3) 1)", [1, 2, 3])

    def test_flatten_once(self):
        self.check("(list-flatten-once '((1 2) 3 ((4)) ()))", [1, 2, 3, [4]])
        self.check("(list-flatten-once '())", [])

    def test_arg(self):
        self.check("(list-argmax '(3 9 2 9))", 1)
        self.check("(list-argmin '(3 1 2 1))", 1)
        self.check("(list-argmax '())", -1)
        self.check("(list-argmin '(5))", 0)


if __name__ == "__main__":
    unittest.main()
