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

; Phase 163

(define (list-twenty-first lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 21) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-eighth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest)
        s
        (let* ((x (car rest)) (x2 (* x x)) (x4 (* x2 x2)))
          (loop (cdr rest) (+ s (* x4 x4)))))))

(define (list-count-multiples-of-six lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((= (remainder (car rest) 6) 0) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sum-multiples-of-six lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 6) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-five lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 5) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-twenty-second lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 22) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-ninth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest)
        s
        (let* ((x (car rest)) (x2 (* x x)) (x4 (* x2 x2)))
          (loop (cdr rest) (+ s (* x (* x4 x4))))))))

(define (list-count-multiples-of-seven lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((= (remainder (car rest) 7) 0) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sum-multiples-of-seven lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 7) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-six lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 6) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-twenty-third lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 23) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-tenth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest)
        s
        (let* ((x (car rest)) (x2 (* x x)) (x4 (* x2 x2)) (x5 (* x4 x)))
          (loop (cdr rest) (+ s (* x5 x5)))))))

(define (list-count-multiples-of-eight lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((= (remainder (car rest) 8) 0) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sum-multiples-of-eight lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 8) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-seven lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 7) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))
