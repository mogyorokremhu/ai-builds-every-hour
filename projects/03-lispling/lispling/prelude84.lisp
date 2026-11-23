; Phase 84: rolling count-at-most-mean/sum-at-most-mean/count-equal-mean/sum-equal-mean
; (put future prelude additions here)
(define (rolling-count-at-most-mean xs n) (map (lambda (w) (let ((s (apply + w)) (c (length w))) (length (filter (lambda (x) (<= (* x c) s)) w)))) (sliding-window xs n)))
(define (rolling-sum-at-most-mean xs n) (map (lambda (w) (let ((s (apply + w)) (c (length w))) (apply + (filter (lambda (x) (<= (* x c) s)) w)))) (sliding-window xs n)))
(define (rolling-count-equal-mean xs n) (map (lambda (w) (let ((s (apply + w)) (c (length w))) (length (filter (lambda (x) (= (* x c) s)) w)))) (sliding-window xs n)))
(define (rolling-sum-equal-mean xs n) (map (lambda (w) (let ((s (apply + w)) (c (length w))) (apply + (filter (lambda (x) (= (* x c) s)) w)))) (sliding-window xs n)))
