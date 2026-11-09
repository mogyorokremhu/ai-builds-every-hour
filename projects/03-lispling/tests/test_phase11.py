import unittest
from lispling import run, global_env
from lispling.vm import run_vm, compile_toplevel, disassemble, NAMES


class InlinePrimTests(unittest.TestCase):
    def check(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_arith_and_compare(self):
        self.check("(define (f a b) (list (+ a b) (- a b) (* a b) (< a b) (>= a b) (= a a))) (f 7 3)",
                   [10, 4, 21, False, True, True])

    def test_emits_prim2(self):
        from lispling.reader import parse
        d = disassemble(compile_toplevel(parse("(lambda (a b) (+ a b))")[0]))
        self.assertIn("PRIM2", d)
        self.assertNotIn("CALL", d)

    def test_variadic_not_inlined(self):
        self.check("(+ 1 2 3 (* 2 2))", 10)
        self.check("(define (f a b c) (+ a b c)) (f 1 2 3)", 6)

    def test_shadowed_by_param(self):
        self.check("(define (f + a b) (+ a b)) (f * 6 7)", 42)

    def test_redefined_global(self):
        self.check("(define (g a b) (+ a b)) (define (+ a b) 99) (g 1 2)", 99)

    def test_tail_loop_still_constant_stack(self):
        self.assertEqual(run_vm("(define (l i a) (if (= i 0) a (l (- i 1) (+ a i)))) (l 50000 0)", global_env()), 1250025000)

    def test_type_error(self):
        from lispling.types import LispError
        with self.assertRaises(LispError):
            run_vm('(+ 1 "a")', global_env())


if __name__ == "__main__":
    unittest.main()
