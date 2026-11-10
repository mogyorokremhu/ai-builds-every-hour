"""Phase 26: char predicates, string comparison/trim helpers, string-map & friends."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestStrings2(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_char_predicates(self):
        self.check('(list (char-alphabetic? "a") (char-numeric? "a") (char-whitespace? " "))', [True, False, True])
        self.check('(list (char-upper-case? "A") (char-lower-case? "A"))', [True, False])

    def test_char_conversion(self):
        self.check('(char->integer "A")', 65)
        self.check('(integer->char 97)', "a")
        self.check('(char-upcase "q")', "Q")
        self.check('(char-downcase "Q")', "q")

    def test_comparisons(self):
        self.check('(list (string>? "b" "a") (string<=? "a" "a") (string>=? "a" "b") (string-ci=? "Ab" "aB"))',
                   [True, True, False, True])

    def test_trim_and_case(self):
        self.check('(string-trim-left "  hi ")', "hi ")
        self.check('(string-trim-right "  hi ")', "  hi")
        self.check('(string-titlecase "hello big world")', "Hello Big World")
        self.check('(string-capitalize "lISP")', "Lisp")

    def test_string_count(self):
        self.check('(string-count "banana" "an")', 2)

    def test_map_filter(self):
        self.check('(string-map char-upcase "abc")', "ABC")
        self.check('(string-filter char-numeric? "a1b2")', "12")

    def test_take_drop(self):
        self.check('(list (string-take "hello" 2) (string-drop "hello" 2))', ["he", "llo"])

    def test_palindrome(self):
        self.check('(palindrome? "Never odd or even")', True)
        self.check('(palindrome? "lisp")', False)

    def test_caesar(self):
        self.check('(caesar-shift 3 "Hello, World!")', "Khoor, Zruog!")
        self.check('(caesar-shift -3 "Khoor")', "Hello")

    def test_word_count(self):
        self.check('(word-count "a  b c")', 3)


if __name__ == "__main__":
    unittest.main()
