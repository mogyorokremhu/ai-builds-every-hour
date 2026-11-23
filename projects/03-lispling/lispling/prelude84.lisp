; Phase 84: rolling count-at-most-mean/sum-at-most-mean/count-equal-mean/sum-equal-mean
; (put future prelude additions here)
(define (rolling-count-at-most-mean xs n) (map (lambda (w) (let ((s (apply + w)) (c (length w))) (length (filter (lambda (x) (<= (* x c) s)) w)))) (sliding-window xs n)))
(define (rolling-sum-at-most-mean xs n) (map (lambda (w) (let ((s (apply + w)) (c (length w))) (apply + (filter (lambda (x) (<= (* x c) s)) w)))) (sliding-window xs n)))
(define (rolling-count-equal-mean xs n) (map (lambda (w) (let ((s (apply + w)) (c (length w))) (length (filter (lambda (x) (= (* x c) s)) w)))) (sliding-window xs n)))
(define (rolling-sum-equal-mean xs n) (map (lambda (w) (let ((s (apply + w)) (c (length w))) (apply + (filter (lambda (x) (= (* x c) s)) w)))) (sliding-window xs n)))
; Phase 85: rolling count/sum of values not equal to the window mean, max-minus-mean and mean-minus-min gaps
(define (rolling-count-not-equal-mean xs n) (map (lambda (w) (let ((s (apply + w)) (c (length w))) (length (filter (lambda (x) (not (= (* x c) s))) w)))) (sliding-window xs n)))
(define (rolling-sum-not-equal-mean xs n) (map (lambda (w) (let ((s (apply + w)) (c (length w))) (apply + (filter (lambda (x) (not (= (* x c) s))) w)))) (sliding-window xs n)))
(define (rolling-max-minus-mean xs n) (map (lambda (w) (- (apply max w) (/ (apply + w) (length w)))) (sliding-window xs n)))
(define (rolling-mean-minus-min xs n) (map (lambda (w) (- (/ (apply + w) (length w)) (apply min w))) (sliding-window xs n)))
; Phase 86: rolling last/first vs mean, max vs last, last vs min gaps
(define (rolling-last-minus-mean xs n) (map (lambda (w) (- (car (reverse w)) (/ (apply + w) (length w)))) (sliding-window xs n)))
(define (rolling-first-minus-mean xs n) (map (lambda (w) (- (car w) (/ (apply + w) (length w)))) (sliding-window xs n)))
(define (rolling-max-minus-last xs n) (map (lambda (w) (- (apply max w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-last-minus-min xs n) (map (lambda (w) (- (car (reverse w)) (apply min w))) (sliding-window xs n)))
; Phase 87: rolling max/min vs first, median vs mean gaps
(define (rolling-max-minus-first xs n) (map (lambda (w) (- (apply max w) (car w))) (sliding-window xs n)))
(define (rolling-first-minus-min xs n) (map (lambda (w) (- (car w) (apply min w))) (sliding-window xs n)))
(define (rolling-median-minus-mean xs n) (map (lambda (w) (- (median w) (/ (apply + w) (length w)))) (sliding-window xs n)))
(define (rolling-mean-minus-median xs n) (map (lambda (w) (- (/ (apply + w) (length w)) (median w))) (sliding-window xs n)))
; Phase 88: rolling last vs first, mean vs max, min vs mean gaps
(define (rolling-last-minus-first xs n) (map (lambda (w) (- (car (reverse w)) (car w))) (sliding-window xs n)))
(define (rolling-first-minus-last xs n) (map (lambda (w) (- (car w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-mean-minus-max xs n) (map (lambda (w) (- (/ (apply + w) (length w)) (apply max w))) (sliding-window xs n)))
(define (rolling-min-minus-mean xs n) (map (lambda (w) (- (apply min w) (/ (apply + w) (length w)))) (sliding-window xs n)))
; Phase 89: rolling median vs max/min/first/last gaps
(define (rolling-max-minus-median xs n) (map (lambda (w) (- (apply max w) (median w))) (sliding-window xs n)))
(define (rolling-median-minus-min xs n) (map (lambda (w) (- (median w) (apply min w))) (sliding-window xs n)))
(define (rolling-median-minus-first xs n) (map (lambda (w) (- (median w) (car w))) (sliding-window xs n)))
(define (rolling-last-minus-median xs n) (map (lambda (w) (- (car (reverse w)) (median w))) (sliding-window xs n)))
; Phase 90: rolling mean vs first/last, min vs median, median vs max gaps
(define (rolling-mean-minus-first xs n) (map (lambda (w) (- (/ (apply + w) (length w)) (car w))) (sliding-window xs n)))
(define (rolling-mean-minus-last xs n) (map (lambda (w) (- (/ (apply + w) (length w)) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-min-minus-median xs n) (map (lambda (w) (- (apply min w) (median w))) (sliding-window xs n)))
(define (rolling-median-minus-max xs n) (map (lambda (w) (- (median w) (apply max w))) (sliding-window xs n)))
