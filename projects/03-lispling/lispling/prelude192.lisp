(define (list-fiftieth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 50) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-thirty-seventh-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 37))))))

(define (list-count-multiples-of-thirty-five lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 35) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-thirty-five lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 35) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-thirty-four lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 34) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

;; ---- phase 193 ----
(define (list-fifty-first lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 51) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-thirty-eighth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 38))))))

(define (list-count-multiples-of-thirty-six lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 36) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-thirty-six lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 36) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-thirty-five lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 35) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

;; ---- phase 194 ----
(define (list-fifty-second lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 52) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-thirty-ninth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 39))))))

(define (list-count-multiples-of-thirty-seven lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 37) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-thirty-seven lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 37) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-thirty-six lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 36) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

;; ---- phase 195 ----
(define (list-fifty-third lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 53) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-fortieth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 40))))))

(define (list-count-multiples-of-thirty-eight lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 38) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-thirty-eight lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 38) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-thirty-seven lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 37) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

;; ---- phase 196 ----
(define (list-fifty-fourth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 54) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-forty-first-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 41))))))

(define (list-count-multiples-of-thirty-nine lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 39) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-thirty-nine lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 39) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-thirty-eight lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 38) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

;; ---- phase 197 ----
(define (list-fifty-fifth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 55) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-forty-second-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 42))))))

(define (list-count-multiples-of-forty lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 40) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-forty lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 40) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-thirty-nine lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 39) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))
