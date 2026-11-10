import unittest
from lispling import run, global_env
from lispling.vm import run_vm


class UtilTests(unittest.TestCase):
    def both(self, src, expect):
        self.assertEqual(run(src, global_env()), expect)
        self.assertEqual(run_vm(src, global_env()), expect)

    def test_take_drop_while(self):
        self.both("(take-while even? '(2 4 5 6))", [2, 4])
        self.both("(drop-while even? '(2 4 5 6))", [5, 6])
        self.both("(take-while even? '())", [])

    def test_filter_map_list_set(self):
        self.both("(filter-map (lambda (x) (and (> x 1) (* x x))) '(1 2 3))", [4, 9])
        self.both("(list-set '(1 2 3) 1 9)", [1, 9, 3])
        self.both("(last-pair '(1 2 3))", [3])

    def test_alist(self):
        self.both("(alist-set '((a 1)) 'b 2)", [[run("'a", global_env()), 1], [run("'b", global_env()), 2]])
        self.both("(alist-ref '((a 1)) 'a 0)", 1)
        self.both("(alist-ref '((a 1)) 'z 0)", 0)

    def test_hash_update_group(self):
        self.both("(let ((h (make-hash))) (hash-update! h 'k inc 0) (hash-update! h 'k inc 0) (hash-ref h 'k))", 2)
        self.both("(length (group-by odd? (iota 6)))", 2)

    def test_strings(self):
        self.both('(string-pad-left "7" 3 "0")', "007")
        self.both('(string-pad-right "ab" 4 ".")', "ab..")
        self.both('(string-prefix? "ab" "abc")', True)
        self.both('(string-suffix? "bc" "abc")', True)
        self.both('(string-suffix? "x" "abc")', False)


if __name__ == "__main__":
    unittest.main()
