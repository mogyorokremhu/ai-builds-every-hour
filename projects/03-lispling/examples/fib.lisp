; Fibonacci two ways.  Run: python repl.py examples/fib.lisp
(define (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2)))))
(define (fib-iter n)
  (let loop ((a 0) (b 1) (i 0))
    (if (= i n) a (loop b (+ a b) (+ i 1)))))
(display "fib 15 =" (fib 15))
(display "fib-iter 90 =" (fib-iter 90))
