import unittest
from lispling import run, global_env
from lispling.vm import run_vm


class FoldTests(unittest.TestCase):
    def both(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_folds(self):
        self.both("(fold-left - 0 '(1 2 3))", -6)
        self.both("(fold-right - 0 '(1 2 3))", 2)
        self.both("(fold-right cons '() '(1 2 3))", [1, 2, 3])
        self.both("(fold-left + 10 '())", 10)

    def test_append_map_iota(self):
        self.both("(append-map (lambda (x) (list x x)) '(1 2))", [1, 1, 2, 2])
        self.both("(iota 4)", [0, 1, 2, 3])
        self.both("(iota-from 3 10)", [10, 11, 12])

    def test_predicates(self):
        self.both("(any even? '(1 3 4))", True)
        self.both("(any even? '())", False)
        self.both("(every odd? '(1 3 5))", True)
        self.both("(every odd? '(1 2))", False)
        self.both("(count even? (iota 10))", 5)

    def test_zip_dedupe(self):
        self.both("(zip '(1 2 3) '(4 5))", [[1, 4], [2, 5]])
        self.both("(remove-duplicates '(1 2 1 3 2))", [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
