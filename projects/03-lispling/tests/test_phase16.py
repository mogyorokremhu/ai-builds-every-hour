import unittest
from lispling import run, global_env
from lispling.vm import run_vm


class LazyTests(unittest.TestCase):
    def check(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_delay_not_run_early(self):
        self.check("(define n 0) (define p (delay (begin (set! n (+ n 1)) n))) n", 0)

    def test_force_memoised(self):
        self.check("(define n 0) (define p (delay (begin (set! n (+ n 1)) n))) (force p) (force p) n", 1)

    def test_force_value(self):
        self.check("(force (delay (* 6 7)))", 42)

    def test_stream_take(self):
        self.check("(stream-take (integers-from 5) 4)", [5, 6, 7, 8])

    def test_stream_filter_map(self):
        self.check("(stream-take (stream-map inc (stream-filter even? (integers-from 0))) 3)", [1, 3, 5])

    def test_stream_ref(self):
        self.check("(stream-ref (integers-from 0) 100)", 100)

    def test_sieve(self):
        self.check("""(define (sieve s) (cons-stream (stream-car s)
          (sieve (stream-filter (lambda (n) (not (= 0 (mod n (stream-car s))))) (stream-cdr s)))))
          (stream-take (sieve (integers-from 2)) 6)""", [2, 3, 5, 7, 11, 13])

    def test_cons_stream_lazy_tail(self):
        self.check("(define s (cons-stream 1 (car '()))) (stream-car s)", 1)


if __name__ == "__main__":
    unittest.main()
