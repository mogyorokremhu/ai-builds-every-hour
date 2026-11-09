; error handling: error, try, assert, when, unless
(define (safe-div a b)
  (try (lambda () (if (= b 0) (error "divide by zero:" a) (/ a b)))
       (lambda (msg) msg)))
(display (safe-div 10 2))
(display (safe-div 7 0))
(when (> 3 2) (display "when ok"))
(unless (> 2 3) (display "unless ok"))
(display (try (lambda () (assert (= 1 2))) (lambda (m) m)))
