import unittest
from lispling.diagnostics import parse_checked, SourceError, tokenize_pos
from lispling.reader import parse


class Positions(unittest.TestCase):
    def test_same_as_parse(self):
        src = "(define (f x) ; hi\n  (* x 'a \"s\"))\n42"
        self.assertEqual(parse_checked(src), parse(src))

    def test_token_positions(self):
        toks = list(tokenize_pos("(a\n  bc)"))
        self.assertEqual(toks[1], ("a", 1, 2))
        self.assertEqual(toks[2], ("bc", 2, 3))

    def test_unclosed(self):
        with self.assertRaises(SourceError) as c:
            parse_checked("(+ 1\n  (* 2 3)")
        self.assertEqual((c.exception.line, c.exception.col), (1, 1))
        self.assertIn("unclosed (", str(c.exception))
        self.assertIn("^", str(c.exception))

    def test_unexpected_close(self):
        with self.assertRaises(SourceError) as c:
            parse_checked("(a)\n  )")
        self.assertEqual((c.exception.line, c.exception.col), (2, 3))

    def test_dangling_quote(self):
        with self.assertRaises(SourceError):
            parse_checked("(a) '")

    def test_unterminated_string(self):
        with self.assertRaises(SourceError) as c:
            parse_checked('(print "oops)')
        self.assertEqual(c.exception.line, 1)


if __name__ == "__main__":
    unittest.main()
