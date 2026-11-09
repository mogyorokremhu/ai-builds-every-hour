import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lispling import run
from lispling.types import LispError


class Forms(unittest.TestCase):
    def test_let_star(self):
        self.assertEqual(run("(let* ((a 2) (b (* a 3))) (+ a b))"), 8)
        self.assertEqual(run("(let* () 5)"), 5)

    def test_letrec(self):
        src = "(letrec ((ev? (lambda (n) (if (= n 0) #t (od? (- n 1))))) (od? (lambda (n) (if (= n 0) #f (ev? (- n 1)))))) (ev? 10))"
        self.assertEqual(run(src), True)

    def test_named_let(self):
        self.assertEqual(run("(let loop ((i 0) (acc 1)) (if (= i 5) acc (loop (+ i 1) (* acc 2))))"), 32)

    def test_named_let_tail_calls(self):
        self.assertEqual(run("(let loop ((i 0)) (if (< i 30000) (loop (+ i 1)) i))"), 30000)

    def test_do(self):
        self.assertEqual(run("(do ((i 0 (+ i 1)) (s 0 (+ s i))) ((= i 5) s))"), 10)
        self.assertEqual(run("(do ((i 0 (+ i 1))) ((= i 3)))"), [])

    def test_quasiquote(self):
        self.assertEqual(run("(define x 5) `(a ,x b)"), ["a", 5, "b"])
        self.assertEqual(run("(define l '(1 2)) `(0 ,@l 3)"), [0, 1, 2, 3])
        self.assertEqual(run("`(1 (2 ,(+ 1 2)))"), [1, [2, 3]])


class Higher(unittest.TestCase):
    def test_map(self):
        self.assertEqual(run("(map (lambda (x) (* x x)) '(1 2 3))"), [1, 4, 9])
        self.assertEqual(run("(map + '(1 2) '(10 20))"), [11, 22])

    def test_filter_reduce(self):
        self.assertEqual(run("(filter (lambda (x) (> x 1)) '(1 2 3))"), [2, 3])
        self.assertEqual(run("(reduce + 0 '(1 2 3 4))"), 10)

    def test_apply(self):
        self.assertEqual(run("(apply + 1 2 '(3 4))"), 10)

    def test_for_each(self):
        from lispling import global_env
        out = []
        run("(for-each display '(1 2))", global_env(out.append))
        self.assertEqual(out, ["1", "2"])

    def test_errors(self):
        for bad in ("(map 1 '(1))", "(apply + 1)", "(filter car 3)"):
            with self.assertRaises(LispError):
                run(bad)


if __name__ == "__main__":
    unittest.main()
