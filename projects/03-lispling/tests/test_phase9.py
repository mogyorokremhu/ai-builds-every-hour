import unittest
from lispling import run, global_env
from lispling.vm import run_vm, compile_toplevel, disassemble
from lispling.reader import parse


class VMExtTests(unittest.TestCase):
    def check(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_named_let(self):
        self.check("(let loop ((i 0) (acc 0)) (if (> i 10) acc (loop (+ i 1) (+ acc i))))", 55)

    def test_named_let_deep_tail(self):
        self.assertEqual(run_vm("(let loop ((i 0)) (if (< i 50000) (loop (+ i 1)) i))", global_env()), 50000)

    def test_let_star_letrec(self):
        self.check("(let* ((a 2) (b (* a 3))) (+ a b))", 8)
        self.check("(letrec ((ev (lambda (n) (if (= n 0) #t (od (- n 1))))) (od (lambda (n) (if (= n 0) #f (ev (- n 1)))))) (ev 10))", True)

    def test_do_loop(self):
        self.check("(do ((i 0 (+ i 1)) (s 0 (+ s i))) ((= i 5) s))", 10)

    def test_quasiquote(self):
        src = "(define x 5) (define l '(1 2)) `(a ,x ,@l b)"
        self.assertEqual(run_vm(src, global_env()), run(src, global_env()))
        self.assertEqual(len(run_vm(src, global_env())), 5)

    def test_constant_folding(self):
        dis = disassemble(compile_toplevel(parse("(+ 1 (* 2 3) (- 10 4))")[0]))
        self.assertIn("CONST    13", dis)
        self.assertNotIn("CALL", dis)
        self.check("(+ 1 (* 2 3) (- 10 4))", 13)

    def test_no_fold_with_variables(self):
        self.check("(define y 4) (+ y (* 2 3))", 10)


if __name__ == "__main__":
    unittest.main()
