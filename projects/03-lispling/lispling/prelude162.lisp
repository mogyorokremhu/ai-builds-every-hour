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

(define (list-twenty-fourth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 24) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-eleventh-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 11))))))

(define (list-count-multiples-of-nine lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 9) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-nine lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 9) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-eight lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 8) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-twenty-fifth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 25) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-twelfth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s
        (loop (cdr rest) (+ s (expt (car rest) 12))))))

(define (list-count-multiples-of-ten lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 10) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-ten lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 10) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-nine lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 9) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-twenty-sixth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 26) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-thirteenth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s
        (loop (cdr rest) (+ s (expt (car rest) 13))))))

(define (list-count-multiples-of-eleven lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 11) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-eleven lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 11) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-ten lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 10) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-twenty-seventh lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 27) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-fourteenth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s
        (loop (cdr rest) (+ s (expt (car rest) 14))))))

(define (list-count-multiples-of-twelve lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 12) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-twelve lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 12) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-eleven lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 11) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-twenty-eighth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 28) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-fifteenth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s
        (loop (cdr rest) (+ s (expt (car rest) 15))))))

(define (list-count-multiples-of-thirteen lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 13) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-thirteen lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 13) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-twelve lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 12) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-twenty-ninth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 29) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-sixteenth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s
        (loop (cdr rest) (+ s (expt (car rest) 16))))))

(define (list-count-multiples-of-fourteen lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 14) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-fourteen lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 14) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-thirteen lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 13) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-thirtieth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 30) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-seventeenth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s
        (loop (cdr rest) (+ s (expt (car rest) 17))))))

(define (list-count-multiples-of-fifteen lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 15) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-fifteen lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 15) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-fourteen lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 14) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-thirty-first lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 31) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-eighteenth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s
        (loop (cdr rest) (+ s (expt (car rest) 18))))))

(define (list-count-multiples-of-sixteen lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 16) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-sixteen lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 16) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-fifteen lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 15) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-thirty-second lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 32) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-nineteenth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s
        (loop (cdr rest) (+ s (expt (car rest) 19))))))

(define (list-count-multiples-of-seventeen lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 17) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-seventeen lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 17) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-sixteen lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 16) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))
