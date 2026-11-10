"""Phase 31: combinatorics and number-theory helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase31(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_factorial_binomial(self):
        self.check("(factorial 0)", 1)
        self.check("(factorial 10)", 3628800)
        self.check("(binomial 10 3)", 120)
        self.check("(binomial 5 7)", 0)

    def test_divisors(self):
        self.check("(divisors 12)", [1, 2, 3, 4, 6, 12])
        self.check("(perfect? 28)", True)
        self.check("(perfect? 12)", False)
        self.check("(totient 36)", 12)

    def test_mod_expt(self):
        self.check("(mod-expt 4 13 497)", 445)
        self.check("(mod-expt 2 10 1000)", 24)

    def test_misc(self):
        self.check("(digits->number '(1 2 3))", 123)
        self.check("(collatz-length 27)", 111)
