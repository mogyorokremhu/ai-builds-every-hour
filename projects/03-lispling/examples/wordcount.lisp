; Count words with a hash table.  Run: python repl.py examples/wordcount.lisp
(define counts (make-hash))
(for-each
  (lambda (w) (hash-set! counts w (+ 1 (hash-ref counts w 0))))
  (string-split "the quick fox jumps over the lazy dog the end"))
(for-each
  (lambda (p) (display (car p) ":" (car (cdr p))))
  (hash->list counts))
