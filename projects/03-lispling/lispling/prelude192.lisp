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

;; ---- phase 198 ----
(define (list-fifty-sixth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 56) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-forty-third-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 43))))))

(define (list-count-multiples-of-forty-one lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 41) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-forty-one lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 41) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-forty lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 40) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

;; ---- phase 199 ----
(define (list-fifty-seventh lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 57) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-forty-fourth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 44))))))

(define (list-count-multiples-of-forty-two lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 42) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-forty-two lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 42) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-forty-one lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 41) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

;; ---- phase 200 ----
(define (list-fifty-eighth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 58) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-forty-fifth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 45))))))

(define (list-count-multiples-of-forty-three lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 43) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-forty-three lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 43) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-forty-two lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 42) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

;; ---- phase 201 ----
(define (list-fifty-ninth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 59) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-forty-sixth-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 46))))))

(define (list-count-multiples-of-forty-four lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 44) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-forty-four lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 44) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-forty-three lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 43) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

;; ---- phase 202 ----
(define (list-sixtieth lst)
  (let loop ((rest lst) (i 1))
    (cond ((null? rest) '())
          ((= i 60) (car rest))
          (else (loop (cdr rest) (+ i 1))))))

(define (list-sum-forty-seventh-powers lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest) s (loop (cdr rest) (+ s (expt (car rest) 47))))))

(define (list-count-multiples-of-forty-five lst)
  (let loop ((rest lst) (n 0))
    (cond ((null? rest) n)
          ((= (remainder (car rest) 45) 0) (loop (cdr rest) (+ n 1)))
          (else (loop (cdr rest) n)))))

(define (list-sum-multiples-of-forty-five lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) 45) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-multiples-of-forty-four lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 44) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))
