; Variadic parameters: (define (f . rest)), (lambda args ...), (lambda (a . r) ...)
(define (sum . xs) (fold-left + 0 xs))
(display (sum 1 2 3 4 5))

(define (tagged tag . items) (map (lambda (i) (list tag i)) items))
(display (tagged 'x 1 2 3))

(define compose
  (lambda fs
    (if (null? fs)
        (lambda (x) x)
        (lambda (x) ((car fs) ((apply compose (cdr fs)) x))))))
(display ((compose square (lambda (n) (+ n 1))) 4))
