"""Phase 24: variadic parameters in both the tree-walker and the VM."""
import unittest

from lispling.evaluator import run
from lispling.types import LispError
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestVariadic(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_lambda_symbol(self):
        self.check("((lambda args args) 1 2 3)", [1, 2, 3])
        self.check("((lambda args args))", [])

    def test_lambda_dotted(self):
        self.check("((lambda (a . r) r) 1 2 3)", [2, 3])
        self.check("((lambda (a b . r) (list a b r)) 1 2)", [1, 2, []])

    def test_define_rest(self):
        self.check("(define (f . xs) (length xs)) (f 1 2 3 4)", 4)
        self.check("(define (g a . xs) (cons a xs)) (g 1 2 3)", [1, 2, 3])

    def test_sum_with_apply(self):
        self.check("(define (sum . xs) (if (null? xs) 0 (+ (car xs) (apply sum (cdr xs))))) (sum 1 2 3 4 5)", 15)

    def test_too_few(self):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                with self.assertRaises(LispError):
                    r("(define (f a b . r) a) (f 1)")

    def test_through_map(self):
        self.check("(define (f . xs) xs) (map f '(1 2 3))", [[1], [2], [3]])

    def test_fixed_still_checked(self):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                with self.assertRaises(LispError):
                    r("((lambda (a) a) 1 2)")


if __name__ == "__main__":
    unittest.main()
