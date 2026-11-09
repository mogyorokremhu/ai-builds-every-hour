import unittest
from lispling import run, global_env
from lispling.types import LispError
from lispling.vm import run_vm, _lookup, Env


class LookupTests(unittest.TestCase):
    def check(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_lookup_walks_chain(self):
        g = Env(); g["x"] = 1
        c = Env(g); c["y"] = 2
        self.assertEqual((_lookup(c, "x"), _lookup(c, "y")), (1, 2))

    def test_lookup_unbound(self):
        with self.assertRaises(LispError):
            _lookup(Env(), "nope")

    def test_unbound_symbol_in_vm(self):
        with self.assertRaises(LispError):
            run_vm("(define (f) zzz) (f)", global_env())

    def test_closure_counter(self):
        self.check("(define (mk) (define n 0) (lambda () (set! n (+ n 1)) n)) "
                   "(define c (mk)) (c) (c) (c)", 3)

    def test_shadowed_prim_inner_scope(self):
        self.check("(define (f + a b) (+ a b)) (f (lambda (a b) (* a b)) 6 7)", 42)

    def test_deep_chain(self):
        self.check("(let ((a 1)) (let ((b 2)) (let ((c 3)) (let ((d 4)) (+ a b c d)))))", 10)

    def test_global_redefinition_seen(self):
        self.check("(define (g x) (car x)) (define (car x) 'mine) (g '(1))", run("'mine", global_env()))


if __name__ == "__main__":
    unittest.main()
