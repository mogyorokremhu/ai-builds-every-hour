import unittest
from lispling import run, global_env
from lispling.types import LispError
from lispling.vm import run_vm


class CaseTests(unittest.TestCase):
    def check(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_match(self):
        self.check("(case (+ 1 1) ((1) 'one) ((2 3) 'few) (else 'many))", __import__("lispling").types.sym("few") if False else run("'few", global_env()))

    def test_else(self):
        self.check("(case 9 ((1) 10) (else 99))", 99)

    def test_no_match_no_else(self):
        self.check("(case 9 ((1) 10))", run("(cond (#f 1))", global_env()))

    def test_key_evaluated_once(self):
        self.check("(define n 0) (define (t) (set! n (+ n 1)) n) (case (t) ((5) 'x) (else n))", 1)

    def test_nested(self):
        self.check("(case 1 ((1) (case 2 ((2) 22) (else 0))) (else 9))", 22)

    def test_strings_and_tail(self):
        self.check('(define (f s i) (case s (("a") (if (= i 0) 7 (f s (- i 1)))) (else 0))) (f "a" 5000)', 7)

    def test_bad_clause(self):
        with self.assertRaises(LispError):
            run("(case 1 (1 2))", global_env())


if __name__ == "__main__":
    unittest.main()
