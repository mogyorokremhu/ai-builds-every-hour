import unittest
from lispling import run, global_env
from lispling.vm import run_vm


class NumericTests(unittest.TestCase):
    def both(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_gcd_lcm(self):
        self.both("(gcd 12 18)", 6)
        self.both("(lcm 4 6)", 12)

    def test_integer_division(self):
        self.both("(quotient -7 2)", -3)
        self.both("(remainder -7 2)", -1)
        self.both("(modulo -7 2)", 1)

    def test_rounding(self):
        self.both("(floor 2.5)", 2)
        self.both("(ceiling 2.1)", 3)
        self.both("(truncate -2.7)", -2)
        self.both("(round 2.5)", 2)
        self.both("(round 3.5)", 4)

    def test_expt_radix(self):
        self.both("(expt 2 10)", 1024)
        self.both('(number->string-radix 255 16)', "ff")
        self.both('(number->string-radix -5 2)', "-101")

    def test_prelude_extras(self):
        self.both("(square 5)", 25)
        self.both("(digits 1234)", [1, 2, 3, 4])
        self.both("(exact-integer-sqrt 50)", 7)
        self.both("(delete-duplicates '(1 2 1 3))", [1, 2, 3])

    def test_errors(self):
        with self.assertRaises(Exception):
            run("(quotient 1 0)", global_env())
        with self.assertRaises(Exception):
            run("(gcd 'a 2)", global_env())


if __name__ == "__main__":
    unittest.main()
