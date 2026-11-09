import unittest
from lispling import run, global_env
from lispling.vm import run_vm, compile_toplevel, disassemble
from lispling.reader import parse
from lispling.types import LispError


class VMMacroTests(unittest.TestCase):
    def check(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_prelude_when_unless(self):
        self.check("(when (> 2 1) 10)", 10)
        self.check("(unless (> 2 1) 10 )", [])

    def test_user_macro(self):
        self.check("(define-macro (twice e) `(begin ,e ,e)) (define n 0) (twice (set! n (+ n 1))) n", 2)

    def test_swap(self):
        self.check("(define a 1) (define b 2) (swap! a b) (list a b)", [2, 1])

    def test_while_loop(self):
        self.check("(define i 0) (define s 0) (while (< i 5) (begin (set! s (+ s i)) (set! i (+ i 1)))) s", 10)

    def test_macro_inside_lambda_and_tail(self):
        src = "(define-macro (my-if c a b) `(cond (,c ,a) (else ,b))) (define (f n) (my-if (= n 0) 0 (f (- n 1)))) (f 20000)"
        self.assertEqual(run_vm(src, global_env()), 0)

    def test_macro_expands_at_compile_time(self):
        env = global_env()
        run_vm("(define-macro (inc1 x) `(+ ,x 1))", env)
        text = disassemble(compile_toplevel(parse("(inc1 4)")[0], env))
        self.assertNotIn("inc1", text)

    def test_arity_error(self):
        with self.assertRaises(LispError):
            run_vm("(define-macro (m a) a) (m 1 2)", global_env())


if __name__ == "__main__":
    unittest.main()
