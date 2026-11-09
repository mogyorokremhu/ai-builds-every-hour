import unittest
from lispling import run, global_env
from lispling.types import LispError, to_string
from lispling.vm import run_vm

POINT = """(define-record-type point (make-point x y) point?
  (x point-x set-point-x!) (y point-y))
"""


class VectorTests(unittest.TestCase):
    def both(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_basic(self):
        self.both("(vector-ref (vector 1 2 3) 1)", 2)
        self.both("(vector-length (make-vector 4 0))", 4)
        self.both("(vector? (vector))", True)
        self.both("(vector? '(1))", False)

    def test_set_and_fill(self):
        self.both("(let ((v (make-vector 3 0))) (vector-set! v 1 9) (vector->list v))", [0, 9, 0])
        self.both("(let ((v (vector 1 2))) (vector-fill! v 7) (vector->list v))", [7, 7])

    def test_conversion_and_print(self):
        self.both("(vector->list (list->vector '(1 2)))", [1, 2])
        self.assertEqual(to_string(run("(vector 1 \"a\" 'b)", global_env())), '#(1 "a" b)')

    def test_equal(self):
        self.both("(equal? (vector 1 2) (vector 1 2))", True)

    def test_range_error(self):
        with self.assertRaises(LispError):
            run("(vector-ref (vector 1) 5)", global_env())
        with self.assertRaises(LispError):
            run("(vector-ref '(1) 0)", global_env())


class RecordTests(unittest.TestCase):
    def both(self, src, expect):
        self.assertEqual(run(POINT + src, global_env()), expect)
        self.assertEqual(run_vm(POINT + src, global_env()), expect)

    def test_construct_access(self):
        self.both("(point-x (make-point 3 4))", 3)
        self.both("(point-y (make-point 3 4))", 4)

    def test_predicate(self):
        self.both("(point? (make-point 1 2))", True)
        self.both("(point? (vector 1 2))", False)
        self.both("(point? 5)", False)

    def test_setter(self):
        self.both("(let ((p (make-point 1 2))) (set-point-x! p 10) (point-x p))", 10)

    def test_wrong_type(self):
        with self.assertRaises(LispError):
            run(POINT + "(point-x 5)", global_env())

    def test_partial_constructor(self):
        src = "(define-record-type c (make-c a) c? (a c-a) (b c-b))(c-b (make-c 1))"
        self.assertEqual(run(src, global_env()), 0)

    def test_bad_spec(self):
        with self.assertRaises(LispError):
            run("(define-record-type p (mk z) p? (x px))", global_env())


if __name__ == "__main__":
    unittest.main()
