import unittest
from lispling import run, global_env
from lispling.types import LispError
from lispling.vm import run_vm, compile_toplevel, disassemble, PRIM2LC


class FusionTests(unittest.TestCase):
    def check(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def ops(self, src):
        code = compile_toplevel(__import__("lispling").reader.parse(src)[0], global_env())
        out = []
        def walk(c):
            for op, arg in c.ops:
                out.append(op)
                if hasattr(arg, "ops"):
                    walk(arg)
        walk(code)
        return out

    def test_fused_op_emitted(self):
        self.assertIn(PRIM2LC, self.ops("(lambda (n) (- n 1))"))

    def test_fib(self):
        self.check("(define (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2))))) (fib 15)", 610)

    def test_loop_tail(self):
        self.check("(define (l i a) (if (= i 0) a (l (- i 1) (+ a i)))) (l 1000 0)", 500500)

    def test_jump_target_not_swallowed(self):
        # the CONST after an `if` is a jump target: must not be fused away
        self.check("(define (f a x y) (+ (if a x y) 1)) (list (f #t 5 6) (f #f 5 6))", [6, 7])

    def test_shadowed_operator(self):
        self.check("(define (f - n) (- n 1)) (f (lambda (a b) (* a b)) 7)", 7)

    def test_redefined_global(self):
        self.check("(define (g n) (+ n 1)) (define (+ a b) 100) (g 5)", 100)

    def test_unbound_var(self):
        with self.assertRaises(LispError):
            run_vm("(define (f) (+ zz 1)) (f)", global_env())

    def test_bad_type(self):
        with self.assertRaises(LispError):
            run_vm("(define (f x) (< x 1)) (f 'a)", global_env())

    def test_disassemble_shows_fused(self):
        c = compile_toplevel(__import__("lispling").reader.parse("(lambda (n) (+ n 2))")[0], global_env())
        self.assertIn("PRIM2LC", disassemble(c))


if __name__ == "__main__":
    unittest.main()
