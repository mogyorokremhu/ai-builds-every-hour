; Phase 162+ list helpers

(define (list-twentieth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 20) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-seventh-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest)
        s
        (let ((x (car rest)))
          (loop (cdr rest) (+ s (* x x x x x x x)))))))

(define (list-count-multiples-of-five lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((= (remainder (car rest) 5) 0) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sum-multiples-of-five lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 5) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-four lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 4) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))
