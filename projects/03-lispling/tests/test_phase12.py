import unittest
from lispling import run, global_env
from lispling.vm import run_vm, compile_toplevel, disassemble
from lispling.reader import parse


class InlineUnaryTests(unittest.TestCase):
    def check(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_basic(self):
        self.check("(define (f l) (list (car l) (cdr l) (null? l) (not l) (pair? l))) (f '(1 2))",
                   [1, [2], False, False, True])

    def test_zero_and_null(self):
        self.check("(list (zero? 0) (zero? 3) (null? '()) (not #f))", [True, False, True, True])

    def test_emits_prim1(self):
        d = disassemble(compile_toplevel(parse("(lambda (l) (car l))")[0]))
        self.assertIn("PRIM1", d)
        self.assertNotIn("CALL", d)

    def test_shadowed_by_param(self):
        self.check("(define (f car x) (car x)) (f (lambda (v) (* v 2)) 21)", 42)

    def test_redefined_global(self):
        self.check("(define (g x) (zero? x)) (define (zero? x) 'no) (g 0)", Symbol_no())

    def test_recursive_length(self):
        self.check("(define (len l) (if (null? l) 0 (+ 1 (len (cdr l))))) (len '(a b c d))", 4)

    def test_tail_loop(self):
        self.assertEqual(run_vm("(define (s l a) (if (null? l) a (s (cdr l) (+ a (car l))))) (s '(1 2 3 4) 0)", global_env()), 10)

    def test_error(self):
        from lispling.types import LispError
        with self.assertRaises(LispError):
            run_vm("(car 5)", global_env())


def Symbol_no():
    from lispling.types import Symbol
    return Symbol("no")


if __name__ == "__main__":
    unittest.main()
