(define (list-thirty-sixth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 36) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-twenty-third-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s
        (loop (cdr rest) (+ s (expt (car rest) 23))))))

(define (list-count-multiples-of-twenty-one lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 21) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-twenty-one lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 21) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-twenty lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 20) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))
