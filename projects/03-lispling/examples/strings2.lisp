;; Strings & chars: map/filter over characters, palindromes, Caesar shift
(display (string-map char-upcase "hello"))
(display (string-filter char-numeric? "a1b22c333"))
(display (palindrome? "A man, a plan, a canal: Panama"))
(display (caesar-shift 3 "Hello, World!"))
(display (caesar-shift -3 (caesar-shift 3 "Round Trip")))
(display (string-capitalize "lispling"))
(display (word-count "the quick  brown fox"))
(string-for-each (lambda (c) (display (char->integer c))) "AB")
