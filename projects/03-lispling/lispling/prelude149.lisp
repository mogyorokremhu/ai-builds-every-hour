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
