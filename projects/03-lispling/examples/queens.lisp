; N-queens solution counter.  Run: python repl.py examples/queens.lisp
; A placement is a list of columns, newest row first.
(define (safe? col placed)
  (let loop ((rest placed) (dist 1))
    (cond ((null? rest) #t)
          ((or (= (car rest) col)
               (= (abs (- (car rest) col)) dist)) #f)
          (else (loop (cdr rest) (+ dist 1))))))
(define (queens n)
  (define (place row placed)
    (if (= row n)
        1
        (let loop ((col 0) (total 0))
          (if (= col n)
              total
              (loop (+ col 1)
                    (if (safe? col placed)
                        (+ total (place (+ row 1) (cons col placed)))
                        total))))))
  (place 0 '()))
(display "6 queens:" (queens 6))
(display "8 queens:" (queens 8))
