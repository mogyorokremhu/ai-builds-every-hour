"""Phase 32: number helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase32(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_gcd_lcm_list(self):
        self.check("(gcd-list '(12 18 24))", 6)
        self.check("(lcm-list '(4 6 10))", 60)

    def test_digits(self):
        self.check("(digit-sum 98765)", 35)
        self.check("(reverse-number 1230)", 321)
        self.check("(palindrome-number? 12321)", True)
        self.check("(palindrome-number? 123)", False)

    def test_roots(self):
        self.check("(triangular 10)", 55)
        self.check("(isqrt 99)", 9)
        self.check("(isqrt 1000000)", 1000)
        self.check("(perfect-square? 144)", True)
        self.check("(perfect-square? 145)", False)

    def test_pascal_happy(self):
        self.check("(pascal-row 4)", [1, 4, 6, 4, 1])
        self.check("(filter happy? (range 1 20))", [1, 7, 10, 13, 19])
