import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lispling import run, global_env
from lispling.types import LispError, to_string


class Strings(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(run('(string-length "hello")'), 5)
        self.assertEqual(run('(substring "hello" 1 3)'), "el")
        self.assertEqual(run('(substring "hello" 2)'), "llo")
        self.assertEqual(run('(string-upcase "abc")'), "ABC")
        self.assertEqual(run('(string-ref "abc" 1)'), "b")

    def test_split_join(self):
        self.assertEqual(run('(string-split "a,b,c" ",")'), ["a", "b", "c"])
        self.assertEqual(run('(string-join (list "a" "b") "-")'), "a-b")
        self.assertEqual(run('(string-join (string-split "x y z"))'), "xyz")

    def test_conversions(self):
        self.assertEqual(run('(string->number "42")'), 42)
        self.assertEqual(run('(string->number "2.5")'), 2.5)
        self.assertIs(run('(string->number "abc")'), False)
        self.assertEqual(run("(number->string 7)"), "7")
        self.assertEqual(run('(symbol->string (quote foo))'), "foo")
        self.assertEqual(run('(symbol? (string->symbol "foo"))'), True)
        self.assertEqual(run('(list->string (reverse (string->list "abc")))'), "cba")

    def test_search(self):
        self.assertTrue(run('(string-contains? "hello" "ell")'))
        self.assertEqual(run('(string-index "hello" "l")'), 2)
        self.assertEqual(run('(string-replace "aXbX" "X" "-")'), "a-b-")

    def test_errors(self):
        with self.assertRaises(LispError):
            run("(string-length 5)")
        with self.assertRaises(LispError):
            run('(substring "abc" 2 9)')
        with self.assertRaises(LispError):
            run('(string-ref "abc" 3)')


class Assoc(unittest.TestCase):
    def test_assoc(self):
        self.assertEqual(run("(assoc 'b '((a 1) (b 2)))"), ["b", 2])
        self.assertIs(run("(assoc 'z '((a 1)))"), False)
        self.assertEqual(run('(assoc "k" (list (list "k" 9)))'), ["k", 9])


class Hash(unittest.TestCase):
    def test_roundtrip(self):
        env = global_env()
        run("(define h (make-hash)) (hash-set! h 'a 1) (hash-set! h \"a\" 2) (hash-set! h '(1 2) 3)", env)
        self.assertEqual(run("(hash-count h)", env), 3)
        self.assertEqual(run("(hash-ref h 'a)", env), 1)
        self.assertEqual(run('(hash-ref h "a")', env), 2)
        self.assertEqual(run("(hash-ref h '(1 2))", env), 3)
        self.assertEqual(run("(hash-ref h 'nope 0)", env), 0)
        self.assertTrue(run("(hash-has-key? h 'a)", env))
        run("(hash-remove! h 'a)", env)
        self.assertFalse(run("(hash-has-key? h 'a)", env))
        self.assertEqual(to_string(run("h", env)), "#<hash-table 2>")

    def test_missing_key_errors(self):
        with self.assertRaises(LispError):
            run("(hash-ref (make-hash) 'x)")

    def test_word_count(self):
        src = """
        (define h (make-hash))
        (for-each (lambda (w) (hash-set! h w (+ 1 (hash-ref h w 0))))
                  (string-split "a b a c a b"))
        (hash-ref h "a")"""
        self.assertEqual(run(src), 3)


if __name__ == "__main__":
    unittest.main()
