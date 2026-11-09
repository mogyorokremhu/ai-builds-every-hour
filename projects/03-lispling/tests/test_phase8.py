import unittest
from lispling import run, global_env
from lispling.vm import run_vm, compile_toplevel, disassemble
from lispling.reader import parse
from lispling.types import LispError


def both(src):
    return run(src, global_env()), run_vm(src, global_env())


class VMTests(unittest.TestCase):
    def check(self, src, expect):
        a, b = both(src)
        self.assertEqual(a, expect)
        self.assertEqual(b, expect)

    def test_arith(self):
        self.check("(+ 1 (* 2 3))", 7)

    def test_if_and_cond(self):
        self.check("(if (< 1 2) 10 20)", 10)
        self.check("(cond ((> 1 2) 1) ((= 1 1) 2) (else 3))", 2)
        self.check("(cond (#f 1) (else 9))", 9)

    def test_define_and_call(self):
        self.check("(define (sq x) (* x x)) (sq 12)", 144)

    def test_fib(self):
        self.check("(define (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2))))) (fib 15)", 610)

    def test_closure_counter(self):
        self.check("(define (mk) (define n 0) (lambda () (set! n (+ n 1)) n))"
                   "(define c (mk)) (c) (c) (c)", 3)

    def test_let(self):
        self.check("(let ((a 2) (b 3)) (* a b))", 6)

    def test_and_or(self):
        self.check("(and 1 2 3)", 3)
        self.check("(and 1 #f 3)", False)
        self.check("(or #f #f 7)", 7)
        self.check("(or)", False)

    def test_deep_tail_call(self):
        self.assertEqual(run_vm("(define (l i) (if (= i 0) 'done (l (- i 1)))) (l 100000)"), "done")

    def test_deep_non_tail_recursion(self):
        # explicit frame stack: no Python RecursionError
        self.assertEqual(run_vm("(define (s n) (if (= n 0) 0 (+ n (s (- n 1))))) (s 5000)"), 12502500)

    def test_and_tail_position(self):
        self.assertEqual(run_vm("(define (f i) (and #t (if (= i 0) 'ok (f (- i 1))))) (f 50000)"), "ok")

    def test_higher_order_interop(self):
        self.check("(map (lambda (x) (* x 2)) '(1 2 3))", [2, 4, 6])

    def test_prelude_interop(self):
        self.check("(reverse '(1 2 3))", [3, 2, 1])

    def test_arity_error(self):
        with self.assertRaises(LispError):
            run_vm("(define (f a) a) (f 1 2)")

    def test_not_procedure(self):
        with self.assertRaises(LispError):
            run_vm("(5 1)")

    def test_disassemble(self):
        text = disassemble(compile_toplevel(parse("(define (f x) (+ x 1))")[0]))
        self.assertIn("MAKE", text)
        self.assertIn("TAILCALL", text)


if __name__ == "__main__":
    unittest.main()
