import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lispling import run, global_env
from lispling.reader import tokenize, parse
from lispling.types import LispError, to_string


class Reader(unittest.TestCase):
    def test_tokens(self):
        self.assertEqual(tokenize("(a 'b) ; hi"), ["(", "a", "'", "b", ")"])

    def test_parse_nested(self):
        self.assertEqual(to_string(parse("(+ 1 (* 2 3.5) \"s\")")[0]), '(+ 1 (* 2 3.5) "s")')

    def test_errors(self):
        for bad in ("(1 2", ")"):
            with self.assertRaises(LispError):
                parse(bad)


class Eval(unittest.TestCase):
    def test_arith(self):
        self.assertEqual(run("(+ 1 2 3)"), 6)
        self.assertEqual(run("(/ 8 2)"), 4)
        self.assertEqual(run("(- 5)"), -5)

    def test_define_and_lambda(self):
        self.assertEqual(run("(define (sq x) (* x x)) (sq 7)"), 49)
        self.assertEqual(run("((lambda (a b) (- a b)) 9 4)"), 5)

    def test_closure(self):
        self.assertEqual(run("(define (adder n) (lambda (x) (+ x n))) ((adder 3) 4)"), 7)

    def test_set_and_begin(self):
        self.assertEqual(run("(define x 1) (set! x 5) (begin x)"), 5)

    def test_cond_let_logic(self):
        self.assertEqual(run("(cond ((< 3 2) 'a) ((> 3 2) 'b) (else 'c))"), "b")
        self.assertEqual(run("(let ((a 2) (b 3)) (* a b))"), 6)
        self.assertEqual(run("(and 1 2 #f 3)"), False)
        self.assertEqual(run("(or #f 7)"), 7)

    def test_lists(self):
        self.assertEqual(run("(cdr (cons 1 (list 2 3)))"), [2, 3])
        self.assertEqual(run("(append '(1) '(2 3))"), [1, 2, 3])
        with self.assertRaises(LispError):
            run("(car '())")

    def test_tail_calls_do_not_overflow(self):
        self.assertEqual(run("(define (loop n a) (if (= n 0) a (loop (- n 1) (+ a 1)))) (loop 50000 0)"), 50000)

    def test_recursion(self):
        self.assertEqual(run("(define (fact n) (if (<= n 1) 1 (* n (fact (- n 1))))) (fact 10)"), 3628800)

    def test_errors(self):
        for bad in ("(foo)", "(1 2)", "(/ 1 0)", "((lambda (x) x))"):
            with self.assertRaises(LispError):
                run(bad)

    def test_display(self):
        out = []
        run('(display "hi" 3)', global_env(out.append))
        self.assertEqual(out, ["hi 3"])


if __name__ == "__main__":
    unittest.main()
