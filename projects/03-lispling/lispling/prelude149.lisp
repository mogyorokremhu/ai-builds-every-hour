; Phase 149+ list helpers

(define (list-seventh lst) (car (cdr (cdr (cdr (cdr (cdr (cdr lst))))))))

(define (list-count-ge n lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((>= (car rest) n) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-count-le n lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((<= (car rest) n) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sum-gt n lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((> (car rest) n) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-sum-lt n lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((< (car rest) n) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

; Phase 150
(define (list-eighth lst) (car (cdr (cdr (cdr (cdr (cdr (cdr (cdr lst)))))))))

(define (list-count-between lo hi lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((and (>= (car rest) lo) (<= (car rest) hi)) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sum-between lo hi lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((and (>= (car rest) lo) (<= (car rest) hi)) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-gt n lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((> (car rest) n) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-count-even lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((even? (car rest)) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-ninth lst) (car (cdr (cdr (cdr (cdr (cdr (cdr (cdr (cdr lst))))))))))

(define (list-count-odd lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((odd? (car rest)) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-count-neq n lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((= (car rest) n) (loop (cdr rest) c))
          (else (loop (cdr rest) (+ c 1))))))

(define (list-sum-ge n lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((>= (car rest) n) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-sum-le n lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((<= (car rest) n) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-tenth lst)
  (list-ref lst 9))

(define (list-product-lt n lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((< (car rest) n) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-product-ge n lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((>= (car rest) n) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-count-divisible d lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((= (remainder (car rest) d) 0) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sum-divisible d lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) d) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-eleventh lst) (list-ref lst 10))

(define (list-count-nonneg lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((>= (car rest) 0) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sum-nonneg lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((>= (car rest) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-even lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 2) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-count-above-mean lst)
  (if (null? lst)
      0
      (let ((n (length lst)) (total (apply + lst)))
        (let loop ((rest lst) (c 0))
          (cond ((null? rest) c)
                ((> (* (car rest) n) total) (loop (cdr rest) (+ c 1)))
                (else (loop (cdr rest) c)))))))

(define (list-twelfth lst)
  (let loop ((rest lst) (n 11))
    (if (= n 0) (car rest) (loop (cdr rest) (- n 1)))))

(define (list-count-nonpos lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((<= (car rest) 0) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sum-nonpos lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((<= (car rest) 0) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-product-odd lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) 2) 0) (loop (cdr rest) p))
          (else (loop (cdr rest) (* p (car rest)))))))

(define (list-count-below-mean lst)
  (if (null? lst)
      0
      (let ((n (length lst)) (total (apply + lst)))
        (let loop ((rest lst) (c 0))
          (cond ((null? rest) c)
                ((< (* (car rest) n) total) (loop (cdr rest) (+ c 1)))
                (else (loop (cdr rest) c)))))))

(define (list-thirteenth lst)
  (let loop ((rest lst) (n 12))
    (if (= n 0) (car rest) (loop (cdr rest) (- n 1)))))

(define (list-sum-above-mean lst)
  (if (null? lst)
      0
      (let ((n (length lst)) (total (apply + lst)))
        (let loop ((rest lst) (s 0))
          (cond ((null? rest) s)
                ((> (* (car rest) n) total) (loop (cdr rest) (+ s (car rest))))
                (else (loop (cdr rest) s)))))))

(define (list-sum-below-mean lst)
  (if (null? lst)
      0
      (let ((n (length lst)) (total (apply + lst)))
        (let loop ((rest lst) (s 0))
          (cond ((null? rest) s)
                ((< (* (car rest) n) total) (loop (cdr rest) (+ s (car rest))))
                (else (loop (cdr rest) s)))))))

(define (list-sum-even-index lst)
  (let loop ((rest lst) (i 0) (s 0))
    (cond ((null? rest) s)
          ((= (remainder i 2) 0) (loop (cdr rest) (+ i 1) (+ s (car rest))))
          (else (loop (cdr rest) (+ i 1) s)))))

(define (list-sum-odd-index lst)
  (let loop ((rest lst) (i 0) (s 0))
    (cond ((null? rest) s)
          ((= (remainder i 2) 1) (loop (cdr rest) (+ i 1) (+ s (car rest))))
          (else (loop (cdr rest) (+ i 1) s)))))

(define (list-fourteenth lst)
  (let loop ((rest lst) (n 13))
    (if (= n 0) (car rest) (loop (cdr rest) (- n 1)))))

(define (list-sum-mod lst k r)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((= (remainder (car rest) k) r) (loop (cdr rest) (+ s (car rest))))
          (else (loop (cdr rest) s)))))

(define (list-count-mod lst k r)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((= (remainder (car rest) k) r) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-product-mod lst k r)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((= (remainder (car rest) k) r) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-count-at-mean lst)
  (if (null? lst)
      0
      (let ((n (length lst)) (total (apply + lst)))
        (let loop ((rest lst) (c 0))
          (cond ((null? rest) c)
                ((= (* (car rest) n) total) (loop (cdr rest) (+ c 1)))
                (else (loop (cdr rest) c)))))))

(define (list-fifteenth lst)
  (let loop ((rest lst) (n 14))
    (if (= n 0) (car rest) (loop (cdr rest) (- n 1)))))

(define (list-count-positive-even lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((and (> (car rest) 0) (even? (car rest))) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sum-squares-odd lst)
  (let loop ((rest lst) (s 0))
    (cond ((null? rest) s)
          ((odd? (car rest)) (loop (cdr rest) (+ s (* (car rest) (car rest)))))
          (else (loop (cdr rest) s)))))

(define (list-weighted-sum lst)
  (let loop ((rest lst) (i 0) (s 0))
    (if (null? rest)
        s
        (loop (cdr rest) (+ i 1) (+ s (* i (car rest)))))))

(define (list-count-prime lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((prime? (car rest)) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sixteenth lst)
  (let loop ((rest lst) (n 15))
    (if (= n 0) (car rest) (loop (cdr rest) (- n 1)))))

(define (list-count-perfect-square lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((perfect-square? (car rest)) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))

(define (list-sum-cubes lst)
  (let loop ((rest lst) (s 0))
    (if (null? rest)
        s
        (loop (cdr rest) (+ s (* (car rest) (car rest) (car rest)))))))

(define (list-product-positive lst)
  (let loop ((rest lst) (p 1))
    (cond ((null? rest) p)
          ((> (car rest) 0) (loop (cdr rest) (* p (car rest))))
          (else (loop (cdr rest) p)))))

(define (list-count-negative-even lst)
  (let loop ((rest lst) (c 0))
    (cond ((null? rest) c)
          ((and (< (car rest) 0) (even? (car rest))) (loop (cdr rest) (+ c 1)))
          (else (loop (cdr rest) c)))))
