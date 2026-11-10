"""Phase 30: number theory and matrix helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase30(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_primes(self):
        self.check("(prime? 97)", True)
        self.check("(prime? 1)", False)
        self.check("(prime? 91)", False)
        self.check("(primes-up-to 20)", [2, 3, 5, 7, 11, 13, 17, 19])

    def test_factors(self):
        self.check("(prime-factors 360)", [2, 2, 2, 3, 3, 5])
        self.check("(prime-factors 97)", [97])

    def test_fib(self):
        self.check("(fib-list 8)", [0, 1, 1, 2, 3, 5, 8, 13])

    def test_matrices(self):
        self.check("(dot-product '(1 2 3) '(4 5 6))", 32)
        self.check("(identity-matrix 2)", [[1, 0], [0, 1]])
        self.check("(mat-mul '((1 2) (3 4)) '((5 6) (7 8)))", [[19, 22], [43, 50]])
        self.check("(mat-pow '((1 1) (1 0)) 10)", [[89, 55], [55, 34]])


if __name__ == "__main__":
    unittest.main()
