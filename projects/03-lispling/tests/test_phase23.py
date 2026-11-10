import unittest
from lispling import run, global_env
from lispling.vm import run_vm


class Phase23Tests(unittest.TestCase):
    def both(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_butlast(self):
        self.both("(length (butlast '(1 2 3)))", 2)
        self.both("(null? (butlast '()))", True)

    def test_curry_flip(self):
        self.both("((curry + 1) 3)", 4)
        self.both("((flip -) 1 10)", 9)

    def test_min_max_by(self):
        self.both("(max-by abs '(1 -5 3))", -5)
        self.both("(min-by abs '(4 -2 3))", -2)

    def test_interleave_transpose(self):
        self.both("(length (interleave '(1 2 3) '(a b)))", 4)
        self.both("(car (cdr (transpose '((1 2) (3 4)))))", run("'(2 4)", global_env()))

    def test_chunk(self):
        self.both("(length (chunk 2 '(1 2 3 4 5)))", 3)

    def test_frequencies(self):
        self.both("(length (frequencies '(a b a c a)))", 3)


if __name__ == "__main__":
    unittest.main()
