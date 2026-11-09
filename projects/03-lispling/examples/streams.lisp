; Infinite streams with cons-stream / delay / force
(define nats (integers-from 0))
(define evens (stream-filter even? nats))
(define squares (stream-map (lambda (n) (* n n)) nats))

(display (stream-take evens 8))
(display (stream-take squares 8))

; sieve of Eratosthenes as a stream
(define (sieve s)
  (cons-stream (stream-car s)
    (sieve (stream-filter (lambda (n) (not (= 0 (mod n (stream-car s))))) (stream-cdr s)))))
(display (stream-take (sieve (integers-from 2)) 12))
