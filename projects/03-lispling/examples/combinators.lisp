; Combinators: variadic curry/partial, constantly, complement, juxt, compose*
(define add5 (curry + 5))
(display (add5 10))
(display (map (partial * 3) '(1 2 3 4)))
(display (filter (complement even?) (iota 10)))
(display ((juxt car cdr length) '(a b c)))
(display ((compose* square (curry + 1) (curry * 2)) 3))
