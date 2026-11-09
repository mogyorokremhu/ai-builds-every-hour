import os, subprocess, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lispling import run, global_env

ROOT = os.path.join(os.path.dirname(__file__), "..")


def example(name):
    r = subprocess.run([sys.executable, "repl.py", f"examples/{name}.lisp"],
                       cwd=ROOT, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    return r.stdout


class TailAudit(unittest.TestCase):
    def test_and_tail(self):
        env = global_env()
        run("(define (f n) (and #t (if (= n 0) 'done (f (- n 1)))))", env)
        self.assertEqual(run("(f 20000)", env), "done")

    def test_or_tail(self):
        env = global_env()
        run("(define (g n) (or #f (if (= n 0) 'done (g (- n 1)))))", env)
        self.assertEqual(run("(g 20000)", env), "done")

    def test_cond_tail(self):
        env = global_env()
        run("(define (h n) (cond ((= n 0) 'done) (else (h (- n 1)))))", env)
        self.assertEqual(run("(h 20000)", env), "done")

    def test_semantics(self):
        self.assertEqual(run("(and)"), True)
        self.assertEqual(run("(or)"), False)
        self.assertEqual(run("(and 1 2 3)"), 3)
        self.assertEqual(run("(and 1 #f 3)"), False)
        self.assertEqual(run("(or #f #f 7)"), 7)
        self.assertEqual(run("(or #f #f #f)"), False)


class Examples(unittest.TestCase):
    def test_fib(self):
        out = example("fib")
        self.assertIn("610", out)
        self.assertIn("2880067194370816120", out)

    def test_primes(self):
        self.assertIn("53 59", example("primes"))

    def test_queens(self):
        out = example("queens")
        self.assertIn("4", out)
        self.assertIn("92", out)


if __name__ == "__main__":
    unittest.main()
