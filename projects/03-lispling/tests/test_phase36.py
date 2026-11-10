"""Phase 36: list helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase36(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_map_indexed(self):
        self.check("(map-indexed (lambda (i x) (* i x)) '(5 6 7))", [0, 6, 14])
        self.check("(map-indexed (lambda (i x) i) '())", [])

    def test_replicate(self):
        self.check("(replicate 3 7)", [7, 7, 7])
        self.check("(replicate 0 7)", [])

    def test_remove_nth(self):
        self.check("(remove-nth '(1 2 3 4) 2)", [1, 2, 4])
        self.check("(remove-nth '(1 2) 9)", [1, 2])

    def test_all_equal(self):
        self.check("(all-equal? '(1 1 1))", True)
        self.check("(all-equal? '(1 2 1))", False)
        self.check("(all-equal? '())", True)

    def test_chunk_by(self):
        self.check("(chunk-by even? '(2 4 1 3 6))", [[2, 4], [1, 3], [6]])
        self.check("(chunk-by even? '())", [])

    def test_cumulative_sum(self):
        self.check("(cumulative-sum '(1 2 3))", [1, 3, 6])


if __name__ == "__main__":
    unittest.main()
