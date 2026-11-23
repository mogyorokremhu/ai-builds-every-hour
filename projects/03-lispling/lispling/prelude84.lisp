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
