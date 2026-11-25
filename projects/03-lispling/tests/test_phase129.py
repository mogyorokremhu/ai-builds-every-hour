"""Phase 129: hash-table helpers."""
import unittest

from lispling.evaluator import run
from lispling.types import sym
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))
SETUP = "(define h (make-hash)) (hash-set! h 'a 1) (hash-set! h 'b 2) (hash-set! h 'c 3) "


class TestPhase129(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(SETUP + expr), expected)

    def test_fold(self):
        self.check("(hash-fold (lambda (acc k v) (+ acc v)) 0 h)", 6)

    def test_filter(self):
        self.check("(hash-count (hash-filter (lambda (k v) (> v 1)) h))", 2)

    def test_map_values(self):
        self.check("(hash-ref (hash-map-values (lambda (v) (* v 10)) h) 'c)", 30)

    def test_copy_independent(self):
        self.check("(let ((c (hash-copy h))) (hash-set! c 'z 9) (hash-count h))", 3)

    def test_merge_and_invert(self):
        self.check("(hash-ref (hash-merge h (hash-invert h)) 2)", sym("b"))
        self.check("(hash-count (hash-merge h h))", 3)


if __name__ == "__main__":
    unittest.main()
