"""Phase 29: search, statistics and in-place vector helpers."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase29(unittest.TestCase):
    def check(self, src, expected):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                self.assertEqual(r(src), expected)

    def test_find(self):
        self.check("(find even? '(1 3 4 5))", 4)
        self.check("(find even? '(1 3))", False)
        self.check("(find-tail even? '(1 4 5))", [4, 5])

    def test_stats(self):
        self.check("(list-max '(3 9 2))", 9)
        self.check("(list-min '(3 9 2))", 2)
        self.check("(average '(1 2 3 4))", 2.5)
        self.check("(median '(5 1 3))", 3)
        self.check("(median '(4 1 3 2))", 2.5)
        self.check("(mode '(1 2 2 3 3 3 1))", 3)

    def test_vectors(self):
        self.check("(let ((v (vector 1 2 3))) (vector-swap! v 0 2) (vector->list v))", [3, 2, 1])
        self.check("(let ((v (vector 1 2 3 4))) (vector-reverse! v) (vector->list v))", [4, 3, 2, 1])

    def test_misc(self):
        self.check("(flatmap (lambda (x) (list x x)) '(1 2))", [1, 1, 2, 2])
        self.check("(reduce-right cons '() '(1 2 3))", [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
