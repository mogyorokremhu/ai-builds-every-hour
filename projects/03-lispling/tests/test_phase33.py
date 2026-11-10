"""Phase 33: sequence helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase33(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_window(self):
        self.check("(length (sliding-window '(1 2 3 4 5) 3))", 3)
        self.check("(car (sliding-window '(1 2 3 4 5) 3))", [1, 2, 3])
        self.check("(sliding-window '(1 2) 3)", [])

    def test_take_every(self):
        self.check("(take-every '(0 1 2 3 4 5 6) 3)", [0, 3, 6])

    def test_rle(self):
        self.check("(rle '(a a b c c c))", [["a", 2], ["b", 1], ["c", 3]])
        self.check("(rle-decode (rle '(1 1 2 3 3)))", [1, 1, 2, 3, 3])
        self.check("(dedupe-adjacent '(1 1 2 2 1))", [1, 2, 1])
        self.check("(rle '())", [])

    def test_scan(self):
        self.check("(scan-left + 0 '(1 2 3 4))", [0, 1, 3, 6, 10])
        self.check("(prefix-sums '(1 2 3 4))", [1, 3, 6, 10])
        self.check("(unfold (lambda (x) (* x 2)) 1 5)", [1, 2, 4, 8, 16])


if __name__ == "__main__":
    unittest.main()
