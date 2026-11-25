"""Phase 132: string-words, string-chunk, string-center, string-vowel-count, string-char-freq."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase132(unittest.TestCase):
    def check(self, expr, expected):
        for rn, r in RUNNERS:
            with self.subTest(runner=rn, expr=expr):
                self.assertEqual(r(expr), expected)

    def test_words(self):
        self.check('(string-words "  the quick  brown fox ")', ["the", "quick", "brown", "fox"])
        self.check('(string-words "")', [])

    def test_chunk(self):
        self.check('(string-chunk "abcdefg" 3)', ["abc", "def", "g"])

    def test_center(self):
        self.check('(string-center "hi" 6)', "  hi  ")
        self.check('(string-center "abc" 2)', "abc")
        self.check('(string-center "a" 4)', " a  ")

    def test_vowels(self):
        self.check('(string-vowel-count "Lispling rocks")', 3)

    def test_char_freq(self):
        self.check('(hash-ref (string-char-freq "banana") "a")', 3)


if __name__ == "__main__":
    unittest.main()
