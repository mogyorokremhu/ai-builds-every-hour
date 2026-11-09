import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lispling import run, global_env
from lispling.types import LispError


class Macros(unittest.TestCase):
    def test_define_macro(self):
        self.assertEqual(run("(define-macro (twice x) `(+ ,x ,x)) (twice 4)"), 8)

    def test_macro_gets_unevaluated(self):
        env = global_env()
        run("(define-macro (my-quote x) `(quote ,x))", env)
        self.assertEqual(run("(my-quote (a b))", env), ["a", "b"])

    def test_macro_arity(self):
        with self.assertRaises(LispError):
            run("(define-macro (m a) a) (m 1 2)")

    def test_recursive_macro_in_tail_position(self):
        src = "(define (f n) (when (> n 0) (f (- n 1)))) (f 20000)"
        self.assertEqual(run(src), [])

    def test_swap(self):
        self.assertEqual(run("(define a 1) (define b 2) (swap! a b) (list a b)"), [2, 1])

    def test_while(self):
        self.assertEqual(run("(define i 0) (while (< i 5) (set! i (+ i 1))) i"), 5)

    def test_unless(self):
        self.assertEqual(run("(unless #f 7)"), 7)
        self.assertEqual(run("(unless #t 7)"), [])


class Prelude(unittest.TestCase):
    def test_lists(self):
        self.assertEqual(run("(reverse '(1 2 3))"), [3, 2, 1])
        self.assertEqual(run("(range 2 6)"), [2, 3, 4, 5])
        self.assertEqual(run("(take '(1 2 3 4) 2)"), [1, 2])
        self.assertEqual(run("(drop '(1 2 3 4) 2)"), [3, 4])
        self.assertEqual(run("(last '(1 2 3))"), 3)
        self.assertEqual(run("(flatten '(1 (2 (3)) 4))"), [1, 2, 3, 4])
        self.assertEqual(run("(member 2 '(1 2 3))"), [2, 3])
        self.assertEqual(run("(member 9 '(1 2 3))"), False)

    def test_numeric(self):
        self.assertEqual(run("(sum (range 1 5))"), 10)
        self.assertTrue(run("(even? 4)"))
        self.assertTrue(run("(odd? 3)"))
        self.assertEqual(run("((compose inc inc) 1)"), 3)

    def test_no_prelude(self):
        env = global_env(prelude=False)
        with self.assertRaises(LispError):
            run("(reverse '(1))", env)


if __name__ == "__main__":
    unittest.main()
