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
; Phase 91: rolling sum vs first/last, median vs last, first vs median gaps
(define (rolling-sum-minus-first xs n) (map (lambda (w) (- (apply + w) (car w))) (sliding-window xs n)))
(define (rolling-sum-minus-last xs n) (map (lambda (w) (- (apply + w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-median-minus-last xs n) (map (lambda (w) (- (median w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-first-minus-median xs n) (map (lambda (w) (- (car w) (median w))) (sliding-window xs n)))
; Phase 92: rolling sum vs max/min/mean/median gaps
(define (rolling-sum-minus-max xs n) (map (lambda (w) (- (apply + w) (apply max w))) (sliding-window xs n)))
(define (rolling-sum-minus-min xs n) (map (lambda (w) (- (apply + w) (apply min w))) (sliding-window xs n)))
(define (rolling-sum-minus-mean xs n) (map (lambda (w) (- (apply + w) (/ (apply + w) (length w)))) (sliding-window xs n)))
(define (rolling-sum-minus-median xs n) (map (lambda (w) (- (apply + w) (median w))) (sliding-window xs n)))

; Phase 93: rolling first/last vs max, min vs first/last
(define (rolling-first-minus-max xs n) (map (lambda (w) (- (car w) (apply max w))) (sliding-window xs n)))
(define (rolling-last-minus-max xs n) (map (lambda (w) (- (car (reverse w)) (apply max w))) (sliding-window xs n)))
(define (rolling-min-minus-first xs n) (map (lambda (w) (- (apply min w) (car w))) (sliding-window xs n)))
(define (rolling-min-minus-last xs n) (map (lambda (w) (- (apply min w) (car (reverse w)))) (sliding-window xs n)))

; Phase 94: rolling first+last, max+min, mean vs sum, median vs sum
(define (rolling-first-plus-last xs n) (map (lambda (w) (+ (car w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-max-plus-min xs n) (map (lambda (w) (+ (apply max w) (apply min w))) (sliding-window xs n)))
(define (rolling-mean-minus-sum xs n) (map (lambda (w) (- (/ (apply + w) (length w)) (apply + w))) (sliding-window xs n)))
(define (rolling-median-minus-sum xs n) (map (lambda (w) (- (median w) (apply + w))) (sliding-window xs n)))

; Phase 95: first+max, last+min, sum+max, sum+min
(define (rolling-first-plus-max xs n) (map (lambda (w) (+ (car w) (apply max w))) (sliding-window xs n)))
(define (rolling-last-plus-min xs n) (map (lambda (w) (+ (car (reverse w)) (apply min w))) (sliding-window xs n)))
(define (rolling-sum-plus-max xs n) (map (lambda (w) (+ (apply + w) (apply max w))) (sliding-window xs n)))
(define (rolling-sum-plus-min xs n) (map (lambda (w) (+ (apply + w) (apply min w))) (sliding-window xs n)))

; Phase 96: first+min, last+max, median+max, median+min
(define (rolling-first-plus-min xs n) (map (lambda (w) (+ (car w) (apply min w))) (sliding-window xs n)))
(define (rolling-last-plus-max xs n) (map (lambda (w) (+ (car (reverse w)) (apply max w))) (sliding-window xs n)))
(define (rolling-median-plus-max xs n) (map (lambda (w) (+ (median w) (apply max w))) (sliding-window xs n)))
(define (rolling-median-plus-min xs n) (map (lambda (w) (+ (median w) (apply min w))) (sliding-window xs n)))

; Phase 97: first+median, last+median, mean+max, mean+min
(define (rolling-first-plus-median xs n) (map (lambda (w) (+ (car w) (median w))) (sliding-window xs n)))
(define (rolling-last-plus-median xs n) (map (lambda (w) (+ (car (reverse w)) (median w))) (sliding-window xs n)))
(define (rolling-mean-plus-max xs n) (map (lambda (w) (+ (/ (apply + w) (length w)) (apply max w))) (sliding-window xs n)))
(define (rolling-mean-plus-min xs n) (map (lambda (w) (+ (/ (apply + w) (length w)) (apply min w))) (sliding-window xs n)))

; Phase 98: mean+median, mean+first, mean+last, sum+median
(define (rolling-mean-plus-median xs n) (map (lambda (w) (+ (/ (apply + w) (length w)) (median w))) (sliding-window xs n)))
(define (rolling-mean-plus-first xs n) (map (lambda (w) (+ (/ (apply + w) (length w)) (car w))) (sliding-window xs n)))
(define (rolling-mean-plus-last xs n) (map (lambda (w) (+ (/ (apply + w) (length w)) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-sum-plus-median xs n) (map (lambda (w) (+ (apply + w) (median w))) (sliding-window xs n)))

; Phase 99: sum+first, sum+last, sum+mean, range+mean
(define (rolling-sum-plus-first xs n) (map (lambda (w) (+ (apply + w) (car w))) (sliding-window xs n)))
(define (rolling-sum-plus-last xs n) (map (lambda (w) (+ (apply + w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-sum-plus-mean xs n) (map (lambda (w) (+ (apply + w) (/ (apply + w) (length w)))) (sliding-window xs n)))
(define (rolling-range-plus-mean xs n) (map (lambda (w) (+ (- (apply max w) (apply min w)) (/ (apply + w) (length w)))) (sliding-window xs n)))

; Phase 100: max+first, max+last, min+first, min+last
(define (rolling-max-plus-first xs n) (map (lambda (w) (+ (apply max w) (car w))) (sliding-window xs n)))
(define (rolling-max-plus-last xs n) (map (lambda (w) (+ (apply max w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-min-plus-first xs n) (map (lambda (w) (+ (apply min w) (car w))) (sliding-window xs n)))
(define (rolling-min-plus-last xs n) (map (lambda (w) (+ (apply min w) (car (reverse w)))) (sliding-window xs n)))

; Phase 101: median+first, median+last, range+first, range+last
(define (rolling-median-plus-first xs n) (map (lambda (w) (+ (median w) (car w))) (sliding-window xs n)))
(define (rolling-median-plus-last xs n) (map (lambda (w) (+ (median w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-range-plus-first xs n) (map (lambda (w) (+ (- (apply max w) (apply min w)) (car w))) (sliding-window xs n)))
(define (rolling-range-plus-last xs n) (map (lambda (w) (+ (- (apply max w) (apply min w)) (car (reverse w)))) (sliding-window xs n)))

; Phase 102: first*last, max*min, range-mean, range-median
(define (rolling-first-times-last xs n) (map (lambda (w) (* (car w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-max-times-min xs n) (map (lambda (w) (* (apply max w) (apply min w))) (sliding-window xs n)))
(define (rolling-range-minus-mean xs n) (map (lambda (w) (- (- (apply max w) (apply min w)) (/ (apply + w) (length w)))) (sliding-window xs n)))
(define (rolling-range-minus-median xs n) (map (lambda (w) (- (- (apply max w) (apply min w)) (median w))) (sliding-window xs n)))

; Phase 103: sum*first, sum*last, mean*first, mean*last
(define (rolling-sum-times-first xs n) (map (lambda (w) (* (apply + w) (car w))) (sliding-window xs n)))
(define (rolling-sum-times-last xs n) (map (lambda (w) (* (apply + w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-mean-times-first xs n) (map (lambda (w) (* (/ (apply + w) (length w)) (car w))) (sliding-window xs n)))
(define (rolling-mean-times-last xs n) (map (lambda (w) (* (/ (apply + w) (length w)) (car (reverse w)))) (sliding-window xs n)))

; Phase 104: median*first, median*last, max*first, max*last
(define (rolling-median-times-first xs n) (map (lambda (w) (* (median w) (car w))) (sliding-window xs n)))
(define (rolling-median-times-last xs n) (map (lambda (w) (* (median w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-max-times-first xs n) (map (lambda (w) (* (apply max w) (car w))) (sliding-window xs n)))
(define (rolling-max-times-last xs n) (map (lambda (w) (* (apply max w) (car (reverse w)))) (sliding-window xs n)))

; Phase 105: min*first, min*last, range*first, range*last
(define (rolling-min-times-first xs n) (map (lambda (w) (* (apply min w) (car w))) (sliding-window xs n)))
(define (rolling-min-times-last xs n) (map (lambda (w) (* (apply min w) (car (reverse w)))) (sliding-window xs n)))
(define (rolling-range-times-first xs n) (map (lambda (w) (* (- (apply max w) (apply min w)) (car w))) (sliding-window xs n)))
(define (rolling-range-times-last xs n) (map (lambda (w) (* (- (apply max w) (apply min w)) (car (reverse w)))) (sliding-window xs n)))

; Phase 106: first*max, first*min, last*max, last*min
(define (rolling-first-times-max xs n) (map (lambda (w) (* (car w) (apply max w))) (sliding-window xs n)))
(define (rolling-first-times-min xs n) (map (lambda (w) (* (car w) (apply min w))) (sliding-window xs n)))
(define (rolling-last-times-max xs n) (map (lambda (w) (* (car (reverse w)) (apply max w))) (sliding-window xs n)))
(define (rolling-last-times-min xs n) (map (lambda (w) (* (car (reverse w)) (apply min w))) (sliding-window xs n)))

; Phase 107: sum*max, sum*min, mean*max, mean*min
(define (rolling-sum-times-max xs n) (map (lambda (w) (* (apply + w) (apply max w))) (sliding-window xs n)))
(define (rolling-sum-times-min xs n) (map (lambda (w) (* (apply + w) (apply min w))) (sliding-window xs n)))
(define (rolling-mean-times-max xs n) (map (lambda (w) (* (/ (apply + w) (length w)) (apply max w))) (sliding-window xs n)))
(define (rolling-mean-times-min xs n) (map (lambda (w) (* (/ (apply + w) (length w)) (apply min w))) (sliding-window xs n)))
