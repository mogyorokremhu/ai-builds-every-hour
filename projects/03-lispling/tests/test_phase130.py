"""Phase 130: hash-pick, hash-omit, hash-any?, hash-every?, hash-from-pairs, hash-count-by."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))
SETUP = "(define h (hash-from-pairs '((a 1) (b 2) (c 3)))) "


class TestPhase130(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(SETUP + expr), expected)

    def test_from_pairs(self):
        self.check("(hash-count h)", 3)

    def test_pick(self):
        self.check("(hash-count (hash-pick h '(a c z)))", 2)

    def test_omit(self):
        self.check("(hash-has-key? (hash-omit h '(a)) 'a)", False)

    def test_any_every(self):
        self.check("(hash-any? (lambda (k v) (> v 2)) h)", True)
        self.check("(hash-every? (lambda (k v) (> v 2)) h)", False)

    def test_count_by(self):
        self.check("(hash-ref (hash-count-by even? '(1 2 3 4 5)) #f)", 3)


if __name__ == "__main__":
    unittest.main()
