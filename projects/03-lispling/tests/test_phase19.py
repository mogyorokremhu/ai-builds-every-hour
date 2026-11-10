import unittest
from lispling import run, global_env
from lispling.types import LispError
from lispling.vm import run_vm


class SortTests(unittest.TestCase):
    def both(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_sort(self):
        self.both("(sort '(3 1 2) <)", [1, 2, 3])
        self.both("(sort '() <)", [])
        self.both("(sort '(1 2 3 4) >)", [4, 3, 2, 1])

    def test_sort_stable(self):
        self.both("(sort '((1 a) (0 b) (1 c) (0 d)) (lambda (x y) (< (car x) (car y))))",
                  run("'((0 b) (0 d) (1 a) (1 c))", global_env()))

    def test_sort_big(self):
        self.both("(sort (map (lambda (i) (mod (* i 7919) 101)) (range 0 60)) <) ",
                  sorted((i * 7919) % 101 for i in range(60)))

    def test_list_utils(self):
        self.both("(list-ref '(a b c) 1)", "b")
        self.both("(list-tail '(1 2 3) 2)", [3])
        self.both("(remove even? '(1 2 3 4))", [1, 3])
        self.both("(delete 2 '(1 2 3 2))", [1, 3])
        self.both("(list-index even? '(1 3 4))", 2)
        self.both("(list-index even? '(1 3))", -1)
        self.both("(partition even? '(1 2 3 4))", [[2, 4], [1, 3]])

    def test_errors(self):
        with self.assertRaises(LispError):
            run("(list-ref '(1) 3)", global_env())

    def test_vectors(self):
        self.both("(vector->list (vector-map inc (vector 1 2)))", [2, 3])
        self.both("(vector->list (vector-sort (vector 3 1 2) <))", [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
