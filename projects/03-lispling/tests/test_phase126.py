"""Phase 126: rolling first, last, max, min to the ninth power."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase126(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_first_ninth(self):
        for v in self.each("(rolling-first-ninth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [1**9,2**9,3**9])

    def test_last_ninth(self):
        for v in self.each("(rolling-last-ninth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [3**9,4**9,5**9])

    def test_max_ninth(self):
        for v in self.each("(rolling-max-ninth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [3**9,4**9,5**9])

    def test_min_ninth(self):
        for v in self.each("(rolling-min-ninth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [1**9,2**9,3**9])


if __name__ == "__main__":
    unittest.main()
