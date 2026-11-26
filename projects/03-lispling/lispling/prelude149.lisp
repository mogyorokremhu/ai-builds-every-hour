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
