; Records and vectors
(define-record-type account (make-account owner balance) account?
  (owner account-owner) (balance account-balance set-account-balance!))

(define (deposit! a n) (set-account-balance! a (+ (account-balance a) n)))

(define a (make-account "ada" 10))
(deposit! a 32)
(display (account-owner a) (account-balance a))

(define v (make-vector 5 0))
(do ((i 0 (+ i 1))) ((= i 5)) (vector-set! v i (* i i)))
(display v)
