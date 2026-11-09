; Sieve-free primes by trial division.  Run: python repl.py examples/primes.lisp
(define (prime? n)
  (and (> n 1)
       (let loop ((d 2))
         (cond ((> (* d d) n) #t)
               ((= 0 (mod n d)) #f)
               (else (loop (+ d 1)))))))
(define (primes-upto n) (filter prime? (range 2 (+ n 1))))
(display (primes-upto 60))
