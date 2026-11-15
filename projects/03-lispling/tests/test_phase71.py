"""Phase 71: rolling-argmax, rolling-argmin, rolling-count-if, rolling-change."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase71(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [int(x) for x in list(r(src))]

    def test_argmax(self):
        for v in self.each("(rolling-argmax '(1 5 2 4 3) 3)"):
            self.assertEqual(v, [1, 0, 1])

    def test_argmin(self):
        for v in self.each("(rolling-argmin '(1 5 2 4 3) 3)"):
            self.assertEqual(v, [0, 1, 0])

    def test_count_if(self):
        for v in self.each("(rolling-count-if even? '(1 2 4 5 6) 2)"):
            self.assertEqual(v, [1, 2, 1, 1])

    def test_change(self):
        for v in self.each("(rolling-change '(1 4 9 16) 2)"):
            self.assertEqual(v, [3, 5, 7])

    def test_short(self):
        for v in self.each("(rolling-change '(1) 2)"):
            self.assertEqual(v, [])


if __name__ == "__main__":
    unittest.main()
