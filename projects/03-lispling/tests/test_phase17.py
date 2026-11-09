import unittest
from lispling import run, global_env
from lispling.types import LispError
from lispling.vm import run_vm


class ErrorFormTests(unittest.TestCase):
    def both(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_when(self):
        self.both("(when (> 2 1) 1 2 3)", 3)
        self.both("(when (< 2 1) 1)", [])

    def test_unless(self):
        self.both("(unless (< 2 1) 5 6)", 6)
        self.both("(unless #t 5)", [])

    def test_when_needs_body(self):
        with self.assertRaises(LispError):
            run("(when #t)", global_env())

    def test_error_raises(self):
        with self.assertRaises(LispError) as c:
            run('(error "boom" 1 "x")', global_env())
        self.assertIn("boom", str(c.exception))

    def test_try_catches(self):
        self.assertEqual(run('(try (lambda () (error "bad")) (lambda (m) m))', global_env()), "bad")

    def test_try_passthrough(self):
        self.assertEqual(run("(try (lambda () 42) (lambda (m) 0))", global_env()), 42)

    def test_try_catches_builtin_errors(self):
        self.assertEqual(run("(try (lambda () (car '())) (lambda (m) 'caught))", global_env()), run("'caught", global_env()))

    def test_assert(self):
        self.assertEqual(run("(assert (= 1 1))", global_env()), True)
        with self.assertRaises(LispError) as c:
            run("(assert (= 1 2))", global_env())
        self.assertIn("assertion failed", str(c.exception))

    def test_assert_in_vm(self):
        self.assertEqual(run_vm("(assert (< 1 2))", global_env()), True)


if __name__ == "__main__":
    unittest.main()
