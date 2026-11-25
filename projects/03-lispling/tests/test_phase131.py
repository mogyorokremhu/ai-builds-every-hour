"""Phase 131: hash-update!, hash-group-by, hash-partition, hash-find-key."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))
SETUP = "(define h (hash-from-pairs '((a 1) (b 2) (c 3)))) "


class TestPhase131(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(SETUP + expr), expected)

    def test_update_existing(self):
        self.check("(hash-ref (hash-update! h 'a (lambda (v) (* v 10)) 0) 'a)", 10)

    def test_update_default(self):
        self.check("(hash-ref (hash-update! h 'z (lambda (v) (+ v 1)) 5) 'z)", 6)

    def test_group_by(self):
        self.check("(hash-ref (hash-group-by even? '(1 2 3 4 5)) #f)", [1, 3, 5])

    def test_partition(self):
        self.check("(let ((p (hash-partition (lambda (k v) (> v 1)) h))) (list (hash-count (car p)) (hash-count (car (cdr p)))))", [2, 1])

    def test_find_key(self):
        self.check("(hash-find-key (lambda (k v) (= v 2)) h)", "b")
        self.check("(hash-find-key (lambda (k v) (> v 9)) h)", False)


if __name__ == "__main__":
    unittest.main()
